# init_db.py
from app.core.database import engine, Base
from app.models.airport import Airport
from app.models.runway import Runway
from app.models.gate import Gate
from app.models.slot import Slot
from app.models.flight import Flight

def init_database():
    print(" Creating database tables...")
    Base.metadata.create_all(engine)
    print("Database tables created!")

if __name__ == "__main__":
    init_database()
