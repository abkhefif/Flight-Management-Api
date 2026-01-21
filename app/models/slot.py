from app.core.database import Base
from sqlalchemy import Column, String, DateTime, ForeignKey
from sqlalchemy import String as UUIDString
from sqlalchemy.orm import relationship
from uuid import uuid4
from sqlalchemy.sql import func

class Slot(Base):
    __tablename__ = "slots"
    
    id = Column(UUIDString(36), primary_key=True, default=lambda: str(uuid4()))
    slot_type = Column(String(20), nullable=False)
    start_time = Column(DateTime, nullable=False)
    end_time = Column(DateTime, nullable=False)
    status = Column(String(20), nullable=False, default="AVAILABLE")
    airport_id = Column(UUIDString(36), ForeignKey("airports.id"), nullable=False, index=True)
    runway_id = Column(UUIDString(36), ForeignKey("runways.id"), nullable=False, index=True)
    flight_id = Column(UUIDString(36), ForeignKey("flights.id"), nullable=True, index=True)
    created_at = Column(DateTime, nullable=False, default=func.now())
    updated_at = Column(DateTime, nullable=False, default=func.now(), onupdate=func.now())
    airport = relationship("Airport", foreign_keys=[airport_id], back_populates="slots")
    runway = relationship("Runway", foreign_keys=[runway_id], back_populates="slots")
    flight = relationship("Flight", foreign_keys=[flight_id], back_populates="slots")
