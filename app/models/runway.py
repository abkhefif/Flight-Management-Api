from app.core.database import Base
from sqlalchemy import Column, String, Integer, DateTime, ForeignKey
from sqlalchemy.orm import relationship
from sqlalchemy import String as UUIDString
from uuid import uuid4
from sqlalchemy.sql import func

class Runway(Base):
    __tablename__= "runways"
    id = Column(UUIDString(36), primary_key=True, default=lambda: str(uuid4()))
    runway_code = Column(String(10), nullable=False)
    length_meters = Column(Integer, nullable=False)
    width_meters = Column(Integer, nullable=False)
    surface_type = Column(String(20), nullable=False)
    status = Column(String(20), nullable=False, default="AVAILABLE")
    airport_id = Column(UUIDString(36), ForeignKey("airports.id"), nullable=False, index=True)
    #foreignKey stock l'id de l'aeroport parent
    created_at = Column(DateTime, nullable=False, default=func.now())
    updated_at = Column(DateTime, nullable=False, default=func.now(), onupdate=func.now())
    airport = relationship("Airport", back_populates="runways")
    slots = relationship("Slot", back_populates="runway")
    #relationship() , avec SqlAlchemy sert a definir une relation entre des objets en DB
    #backpopulates est un lien bidirectionnel , Relationship() est necessaire des deux cotes, ici Airport et Runway
