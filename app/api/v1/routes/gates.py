from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from typing import List

from app.core.database import SessionLocal
from app.schemas.gate import GateRead, GateCreate, GateUpdate
from app.models.gate import Gate

router = APIRouter()

def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()

#GET ALL
@router.get("", response_model = List[GateRead])
def get_gates(db:Session = Depends(get_db)):
    gates = db.query(Gate).all()
    return gates

#GET ONE
@router.get("/{id}", response_model = GateRead)
def get_gate(id: str , db: Session = Depends(get_db)):
    gate = db.query(Gate).filter(Gate.id == id).first()
    if not gate:
        raise HTTPException(status_code=404, detail="Gate not found")
    return gate

#POST
@router.post("", response_model = GateRead, status_code = 201)
def create_gate(gate: GateCreate, db: Session = Depends(get_db)):
    db_gate = Gate(**gate.dict())
    db.add(db_gate)
    db.commit()
    db.refresh(db_gate)
    return db_gate

#PUT
@router.put("/{id}", response_model = GateRead)
def  update_gate(id: str, gate_update: GateUpdate, db: Session = Depends(get_db)):
    gate = db.query(Gate).filter(Gate.id == id).first()
    if not gate:
        raise HTTPException(status_code = 404, detail="Gate not found")
    for key, value in gate_update.dict(exclude_unset=True).items():
        setattr(gate, key, value)
    db.commit()
    db.refresh(gate)
    return gate

#DElETE
@router.delete("/{id}")
def delete_gate(id:str, db: Session = Depends(get_db)):
    gate = db.query(Gate).filter(Gate.id == id).first()
    if not gate:
        raise HTTPException(status_code = 404, detail="Gate not found")
    db.delete(gate)
    db.commit()
    return {"message" : "Gate deleted successfully"}

