from app.core.database import SessionLocal
from datetime import datetime, timedelta
from uuid import uuid4

def seed_database():
    # Import ICI, pas en haut du fichier !
    from app.models.airport import Airport
    from app.models.runway import Runway
    from app.models.gate import Gate
    from app.models.flight import Flight
    db = SessionLocal()
    
    try:
        # Vérifier si des données existent déjà
        existing_airports = db.query(Airport).count()
        if existing_airports > 0:
            print("✅ Database already has data, skipping seed...")
            return
        
        print("🌱 Seeding database with demo data...")
        
        # ========== AIRPORTS ==========
        cdg = Airport(
            id=str(uuid4()),
            code="CDG",
            name="Charles de Gaulle Airport",
            city="Paris",
            country="France",
            timezone="Europe/Paris"
        )
        
        jfk = Airport(
            id=str(uuid4()),
            code="JFK",
            name="John F. Kennedy International Airport",
            city="New York",
            country="USA",
            timezone="America/New_York"
        )
        
        lhr = Airport(
            id=str(uuid4()),
            code="LHR",
            name="London Heathrow Airport",
            city="London",
            country="United Kingdom",
            timezone="Europe/London"
        )
        
        nrt = Airport(
            id=str(uuid4()),
            code="NRT",
            name="Narita International Airport",
            city="Tokyo",
            country="Japan",
            timezone="Asia/Tokyo"
        )
        
        db.add_all([cdg, jfk, lhr, nrt])
        db.commit()
        print("  ✅ Added 4 airports")
        
        # ========== RUNWAYS ==========
        cdg_runway1 = Runway(
            id=str(uuid4()),
            runway_code="09L/27R",
            length_meters=4200,
            width_meters=45,
            surface_type="asphalt",
            status="AVAILABLE",
            airport_id=cdg.id
        )
        
        cdg_runway2 = Runway(
            id=str(uuid4()),
            runway_code="09R/27L",
            length_meters=4215,
            width_meters=45,
            surface_type="asphalt",
            status="AVAILABLE",
            airport_id=cdg.id
        )
        
        jfk_runway = Runway(
            id=str(uuid4()),
            runway_code="04L/22R",
            length_meters=3682,
            width_meters=46,
            surface_type="asphalt",
            status="AVAILABLE",
            airport_id=jfk.id
        )
        
        lhr_runway = Runway(
            id=str(uuid4()),
            runway_code="09L/27R",
            length_meters=3902,
            width_meters=50,
            surface_type="asphalt",
            status="AVAILABLE",
            airport_id=lhr.id
        )
        
        nrt_runway = Runway(
            id=str(uuid4()),
            runway_code="16R/34L",
            length_meters=4000,
            width_meters=60,
            surface_type="asphalt",
            status="AVAILABLE",
            airport_id=nrt.id
        )
        
        db.add_all([cdg_runway1, cdg_runway2, jfk_runway, lhr_runway, nrt_runway])
        db.commit()
        print("  ✅ Added 5 runways")
        
        # ========== GATES ==========
        gates = [
            Gate(id=str(uuid4()), gate_code="A1", terminal="Terminal 2E", status="AVAILABLE", gate_type="INTERNATIONAL", airport_id=cdg.id),
            Gate(id=str(uuid4()), gate_code="A2", terminal="Terminal 2E", status="AVAILABLE", gate_type="INTERNATIONAL", airport_id=cdg.id),
            Gate(id=str(uuid4()), gate_code="B12", terminal="Terminal 4", status="AVAILABLE", gate_type="INTERNATIONAL", airport_id=jfk.id),
            Gate(id=str(uuid4()), gate_code="T5-10", terminal="Terminal 5", status="AVAILABLE", gate_type="INTERNATIONAL", airport_id=lhr.id),
            Gate(id=str(uuid4()), gate_code="S20", terminal="Terminal 1", status="AVAILABLE", gate_type="INTERNATIONAL", airport_id=nrt.id),
        ]
        
        db.add_all(gates)
        db.commit()
        print("  ✅ Added 5 gates")
        
        # ========== FLIGHTS (avec slots automatiques via FlightService) ==========
        from app.services.flight_service import FlightService
        from app.schemas.flight import FlightCreate
        
        now = datetime.utcnow()
        
        flights_data = [
            {
                "flight_number": "AF001",
                "airline": "Air France",
                "departure_airport_id": cdg.id,
                "arrival_airport_id": jfk.id,
                "scheduled_departure": now + timedelta(hours=2),
                "scheduled_arrival": now + timedelta(hours=10),
                "status": "SCHEDULED"
            },
            {
                "flight_number": "BA178",
                "airline": "British Airways",
                "departure_airport_id": lhr.id,
                "arrival_airport_id": jfk.id,
                "scheduled_departure": now + timedelta(hours=4),
                "scheduled_arrival": now + timedelta(hours=12),
                "status": "SCHEDULED"
            },
            {
                "flight_number": "JL006",
                "airline": "Japan Airlines",
                "departure_airport_id": nrt.id,
                "arrival_airport_id": cdg.id,
                "scheduled_departure": now + timedelta(hours=6),
                "scheduled_arrival": now + timedelta(hours=18),
                "status": "SCHEDULED"
            }
        ]
        
        for flight_data in flights_data:
            flight_create = FlightCreate(**flight_data)
            FlightService.create(flight_create, db)
        
        print("  ✅ Added 3 flights (with automatic slots)")
        
        print("\n🎉 Database seeded successfully!")
        print("\n📊 Demo data summary:")
        print(f"  - Airports: {db.query(Airport).count()}")
        print(f"  - Runways: {db.query(Runway).count()}")
        print(f"  - Gates: {db.query(Gate).count()}")
        print(f"  - Flights: {db.query(Flight).count()}")
        
    except Exception as e:
        print(f"❌ Error seeding database: {e}")
        db.rollback()
    finally:
        db.close()

if __name__ == "__main__":
    seed_database()
