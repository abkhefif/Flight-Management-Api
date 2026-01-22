from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from typing import List

from app.core.database import get_db
from app.schemas.runway import RunwayRead, RunwayCreate, RunwayUpdate
from app.models.runway import Runway

router = APIRouter()

#def get_db():
 #   db = SessionLocal()
  #  try:
   #     yield db
    #finally:
     #   db.close()

#GET ALL
@router.get("", response_model = List[RunwayRead])
def get_runways(db:Session = Depends(get_db)):
    runways = db.query(Runway).all()
    return runways

#GET ONE
@router.get("/{id}", response_model = RunwayRead)
def get_runway(id: str , db: Session = Depends(get_db)):
    runway = db.query(Runway).filter(Runway.id == id).first()
    if not runway:
        raise HTTPException(status_code=404, detail="Runway not found")
    return runway

#POST
@router.post("", response_model = RunwayRead, status_code = 201)
def create_runway(runway: RunwayCreate, db: Session = Depends(get_db)):
    db_runway = Runway(**runway.dict())
    db.add(db_runway)
    db.commit()
    db.refresh(db_runway)
    return db_runway

#PUT
@router.put("/{id}", response_model = RunwayRead)
def  update_runway(id: str, runway_update: RunwayUpdate, db: Session = Depends(get_db)):
    runway = db.query(Runway).filter(Runway.id == id).first()
    if not runway:
        raise HTTPException(status_code = 404, detail="Runway not found")
    for key, value in runway_update.dict(exclude_unset=True).items():
        setattr(runway, key, value)
    db.commit()
    db.refresh(runway)
    return runway

#DElETE
@router.delete("/{id}")
def delete_runway(id:str, db: Session = Depends(get_db)):
    runway = db.query(Runway).filter(Runway.id == id).first()
    if not runway:
        raise HTTPException(status_code = 404, detail="Runway not found")
    db.delete(runway)
    db.commit()
    return {"message" : "Runway deleted successfully"}

