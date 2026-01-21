from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from typing import List
from app.services.flight_service import FlightService
from app.core.database import SessionLocal
from app.schemas.flight import FlightRead, FlightCreate, FlightUpdate
from app.models.flight import Flight
from uuid import UUID

router = APIRouter()

def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()

#GET ALL
@router.get("", response_model = List[FlightRead])
def get_flights(db:Session = Depends(get_db)):
    flights = db.query(Flight).all()
    return flights

#GET ONE
@router.get("/{id}", response_model = FlightRead)
def get_flight(id: str , db: Session = Depends(get_db)):
    flight = db.query(Flight).filter(Flight.id == id).first()
    if not flight:
        raise HTTPException(status_code=404, detail="Flight not found")
    return flight

#POST
@router.post("", response_model = FlightRead, status_code = 201)
def create_flight(flight: FlightCreate, db: Session = Depends(get_db)):
    return FlightService.create(flight, db)
#PUT
@router.put("/{id}", response_model = FlightRead)
def  update_flight(id: str, flight_update: FlightUpdate, db: Session = Depends(get_db)):
    flight = db.query(Flight).filter(Flight.id == id).first()
    if not flight:
        raise HTTPException(status_code = 404, detail="Flight not found")
    update_data = flight_update.dict(exclude_unset=True)
    for key, value in flight_update.dict(exclude_unset=True).items():
        if isinstance(value, UUID):
            update_data[key] = str(value)
        setattr(flight, key, value)
    db.commit()
    db.refresh(flight)
    return flight

#DElETE
@router.delete("/{id}")
def delete_flight(id:str, db: Session = Depends(get_db)):
    flight = db.query(Flight).filter(Flight.id == id).first()
    if not flight:
        raise HTTPException(status_code = 404, detail="Flight not found")
    db.delete(flight)
    db.commit()
    return {"message" : "Flight deleted successfully"}

