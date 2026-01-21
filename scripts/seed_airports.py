from app.core.database import SessionLocal
from app.models.airport import Airport
from app.models.runway import Runway

db = SessionLocal()
list_airports = [
    {"code" : "ORY" , "name" : "Orly Airport" ,  "city" : "Paris" , "country" : "FRA" , "timezone" : "Europe/Paris"
    },
    {"code" : "JFK", "name" : "John F. Kennedy International", "city" : "New York", "country" : "USA", "timezone" : "America/New_York"
    },
    {"code" : "NRT", "name" : "Narita International", "city" : "Tokyo", "country" : "JPN", "timezone" : "Asia/Tokyo"
    },
    {"code" : "LHR" , "name" : "Heartrow Airport", "city" : "London", "country" : "GBR", "timezone" : "Europe/London"
    }
]

for airport_data in list_airports:
    airport = Airport(**airport_data)
    db.add(airport)

db.commit()
print("Commit ok!")
db.close()
