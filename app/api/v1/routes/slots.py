from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from typing import List
from uuid import UUID
from app.core.database import get_db
from app.schemas.slot import SlotRead, SlotCreate, SlotUpdate
from app.models.slot import Slot

router = APIRouter()

#GET ALL
@router.get("", response_model = List[SlotRead])
def get_slots(db:Session = Depends(get_db)):
    slots = db.query(Slot).all()
    return slots

#GET ONE
@router.get("/{id}", response_model = SlotRead)
def get_slot(id: str , db: Session = Depends(get_db)):
    slot = db.query(Slot).filter(Slot.id == id).first()
    if not slot:
        raise HTTPException(status_code=404, detail="Slot not found")
    return slot

#POST
@router.post("", response_model = SlotRead, status_code = 201)
def create_slot(slot: SlotCreate, db: Session = Depends(get_db)):
    slot_data = slot.model_dump()
    for key, value in slot_data.items():
        if isinstance(value, UUID):
            slot_data[key] = str(value)
    db_slot = Slot(**slot_data)
    db.add(db_slot)
    db.commit()
    db.refresh(db_slot)
    return db_slot

#PUT
@router.put("/{id}", response_model = SlotRead)
def  update_slot(id: str, slot_update: SlotUpdate, db: Session = Depends(get_db)):
    slot = db.query(Slot).filter(Slot.id == id).first()
    if not slot:
        raise HTTPException(status_code = 404, detail="Slot not found")
    for key, value in slot_update.dict(exclude_unset=True).items():
        setattr(slot, key, value)
    db.commit()
    db.refresh(slot)
    return slot

#DElETE
@router.delete("/{id}")
def delete_slot(id:str, db: Session = Depends(get_db)):
    slot = db.query(Slot).filter(Slot.id == id).first()
    if not slot:
        raise HTTPException(status_code = 404, detail="Slot not found")
    db.delete(slot)
    db.commit()
    return {"message" : "Slot deleted successfully"}

