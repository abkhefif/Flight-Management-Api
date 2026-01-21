from sqlalchemy import Column, String, DateTime, ForeignKey
from sqlalchemy import String as UUIDString
from app.models.gate import Gate
from app.core.database import Base
from sqlalchemy.orm import relationship
from uuid import uuid4
from sqlalchemy.sql import func

class Flight(Base):
    __tablename__ = "flights"
    id = Column(UUIDString(36), primary_key = True, default=lambda: str(uuid4()))
    flight_number = Column(String(10), nullable=False, unique=True, index=True)
    #ex vol AF123 doit etre UNIQUE!
    airline = Column(String(100),nullable=False)
    departure_airport_id = Column(UUIDString(36),ForeignKey("airports.id"),nullable=False, index=True)
    arrival_airport_id = Column(UUIDString(36),ForeignKey("airports.id"),nullable=False, index=True)
    departure_gate_id = Column(UUIDString(36),ForeignKey("gates.id"), nullable=True,index=True)
    arrival_gate_id = Column(UUIDString(36),ForeignKey("gates.id"), nullable=True,index=True)
    scheduled_departure = Column(DateTime,nullable=False)
    scheduled_arrival = Column(DateTime,nullable=False)
    actual_departure = Column(DateTime, nullable=True)
    actual_arrival = Column(DateTime,nullable=True)
    status = Column(String(20),nullable=False, default="SCHEDULED")
    created_at = Column(DateTime, nullable=False, default=func.now())
    updated_at = Column(DateTime, nullable=False, default=func.now(), onupdate=func.now())
    departure_airport = relationship("Airport", foreign_keys=[departure_airport_id], back_populates="departing_flights")
    arrival_airport = relationship("Airport", foreign_keys=[arrival_airport_id], back_populates="arriving_flights")
    departure_gate = relationship("Gate", foreign_keys=[departure_gate_id], back_populates="departing_flights")
    arrival_gate = relationship("Gate", foreign_keys=[arrival_gate_id], back_populates="arriving_flights")
    slots = relationship("Slot", back_populates="flight")
