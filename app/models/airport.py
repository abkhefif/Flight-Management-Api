from app.core.database import Base
from sqlalchemy import Column, String, DateTime
from sqlalchemy import String as UUIDString
from sqlalchemy.dialects.postgresql import UUID as PostgresUUID
from uuid import uuid4
from sqlalchemy.sql import func
from sqlalchemy.orm import relationship

class Airport(Base):
    __tablename__ = "airports"
    id = Column(UUIDString(36), primary_key=True, default=lambda: str(uuid4()))
#uuid == le type,au format hexadecimal, valeur unique, securised, generer client side
#as_uuid = true == stocker comme un uuid et le manipule comme un objet uuid.UUID 
#primary key == id unique a chaque ligne, ne peut etre null
# default=uuid4 == si pas d'id founit, appel uuid4() pour en generate un auto
#uuid est pour le syst aero/def est used car tres safety, n'expose pas le nb d'entité, standard , evite les colisions
    code = Column(String(4), unique=True, nullable=False, index=True)
    name = Column(String(255), nullable=False)
    city = Column(String(255), nullable=False)
    country = Column(String(100), nullable=False)
    timezone = Column(String(50), nullable=False)
    created_at = Column(DateTime, nullable=False, default=func.now())
    updated_at = Column(DateTime, nullable=False, default=func.now(),onupdate=func.now()) 
    runways = relationship("Runway", back_populates="airport")
    gates = relationship("Gate", back_populates="airport")
    departing_flights = relationship("Flight", foreign_keys="[Flight.departure_airport_id]", back_populates="departure_airport")
    arriving_flights = relationship("Flight", foreign_keys="[Flight.arrival_airport_id]", back_populates="arrival_airport")
    slots = relationship("Slot", back_populates="airport")
