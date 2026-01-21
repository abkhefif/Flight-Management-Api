from sqlalchemy import Column, String, DateTime, ForeignKey
from sqlalchemy import String as UUIDString
from app.core.database import Base
from sqlalchemy.orm import relationship
from uuid import uuid4
from sqlalchemy.sql import func

class Gate(Base):
    __tablename__ = "gates"
    id = Column(UUIDString(36), primary_key = True, default=lambda: str(uuid4()))
    gate_code = Column(String(10), nullable = False)
    terminal = Column(String(10), nullable = False)
    status = Column(String(20), nullable = False, default = "AVAILABLE")
    gate_type = Column(String(20), nullable=False)
    airport_id = Column(UUIDString(36),ForeignKey("airports.id"), nullable= False, index=True)
    created_at = Column(DateTime,nullable = False , default=func.now())
    updated_at = Column(DateTime, nullable = False, default=func.now(), onupdate=func.now())
    airport = relationship("Airport", back_populates="gates")
    departing_flights = relationship("Flight", foreign_keys="[Flight.departure_gate_id]", back_populates="departure_gate")
    arriving_flights = relationship("Flight", foreign_keys="[Flight.arrival_gate_id]", back_populates="arrival_gate")
