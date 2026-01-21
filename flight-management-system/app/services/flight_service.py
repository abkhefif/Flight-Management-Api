from sqlalchemy.orm import Session
from uuid import UUID
from app.models.flight import Flight
from app.schemas.flight import FlightCreate
from app.models.runway import Runway
from app.models.slot import Slot
from datetime import timedelta, datetime
from fastapi import HTTPException

def check_runway_conflict(runway_id: str, start_time: datetime, end_time: datetime, db: Session):
    conflict = db.query(Slot).filter(Slot.runway_id == runway_id, Slot.status == "ALLOCATED", Slot.start_time < end_time, Slot.end_time > start_time).first()
    return conflict is not None
class FlightService:

    @staticmethod
    def create(flight: FlightCreate, db:Session):
        flight_data = flight.model_dump()
        for key, value in flight_data.items():
            if isinstance(value, UUID):
                flight_data[key] = str(value)
        db_flight = Flight(**flight_data)
        db.add(db_flight)
        db.flush() #flush au lieu de commit pour avoir l'id mais pas encore sauvegarder 
        available_departure_runway = db.query(Runway).filter(Runway.airport_id == str(db_flight.departure_airport_id), Runway.status == "AVAILABLE").first()
        if not available_departure_runway:
            db.rollback()
            raise HTTPException(400, "No runway available")
        departure_start = flight.scheduled_departure - timedelta(minutes=30)
        departure_end = flight.scheduled_departure + timedelta(minutes=15)
        if check_runway_conflict(str(available_departure_runway.id), departure_start, departure_end, db):
            db.rollback()
            raise HTTPException(409, "Runway conflict at departure airport")
        departure_slot = Slot(
            slot_type="DEPARTURE",
            start_time=departure_start,
            end_time=departure_end,
            status="ALLOCATED",
            airport_id=str(flight.departure_airport_id),
            runway_id=str(available_departure_runway.id),
            flight_id=str(db_flight.id)
                )
        db.add(departure_slot)
        
        available_arrival_runway = db.query(Runway).filter(Runway.airport_id == str(db_flight.arrival_airport_id), Runway.status == "AVAILABLE").first()
        if not available_arrival_runway:
            db.rollback()
            raise HTTPException(400, "No runway available")
        arrival_start = flight.scheduled_arrival - timedelta(minutes=30)
        arrival_end = flight.scheduled_arrival + timedelta(minutes=15)
        if check_runway_conflict(str(available_arrival_runway.id), arrival_start, arrival_end, db):
            db.rollback()
            raise HTTPException(409, "Runway conflict at arrival airport")
        arrival_slot = Slot(
            slot_type="ARRIVAL",
            start_time=arrival_start,
            end_time=arrival_end,
            status="ALLOCATED",
            airport_id=str(flight.arrival_airport_id),
            runway_id=str(available_arrival_runway.id),
            flight_id=str(db_flight.id)
                )
        db.add(arrival_slot)
        db.commit()
        db.refresh(db_flight)
        return db_flight
