from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from typing import List

from app.core.database import get_db
from app.schemas.airport import AirportRead, AirportCreate, AirportUpdate
from app.models.airport import Airport

router = APIRouter()

# 1. GET ALL
@router.get("", response_model=List[AirportRead])
def get_airports(db: Session = Depends(get_db)):
    airports = db.query(Airport).all()
    return airports

# 2. GET ONE
@router.get("/{id}", response_model=AirportRead)
def get_airport(id: str, db: Session = Depends(get_db)):
    airport = db.query(Airport).filter(Airport.id == id).first()
    if not airport:
        raise HTTPException(status_code=404, detail="Airport not found")
    return airport

# 3. POST
@router.post("", response_model=AirportRead, status_code=201)
def create_airport(airport: AirportCreate, db: Session = Depends(get_db)):
    db_airport = Airport(**airport.dict())
    db.add(db_airport)
    db.commit()
    db.refresh(db_airport)
    return db_airport

# 4. PUT
@router.put("/{id}", response_model=AirportRead)
def update_airport(id: str, airport_update: AirportUpdate, db: Session = Depends(get_db)):
    airport = db.query(Airport).filter(Airport.id == id).first()
    if not airport:
        raise HTTPException(status_code=404, detail="Airport not found")
    
    for key, value in airport_update.dict(exclude_unset=True).items():
        setattr(airport, key, value)
    
    db.commit()
    db.refresh(airport)
    return airport

# 5. DELETE
@router.delete("/{id}")
def delete_airport(id: str, db: Session = Depends(get_db)):
    airport = db.query(Airport).filter(Airport.id == id).first()
    if not airport:
        raise HTTPException(status_code=404, detail="Airport not found")
    
    db.delete(airport)
    db.commit()
    return {"message": "Airport deleted successfully"}
