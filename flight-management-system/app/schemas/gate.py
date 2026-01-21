from pydantic import BaseModel, ConfigDict
from typing import Optional
from uuid import UUID
from datetime import datetime

class GateCreate(BaseModel):
    gate_code : str
    terminal : str
    status : str
    gate_type : str
    airport_id : str

class GateRead(BaseModel):
    id : UUID
    gate_code : str
    terminal : str
    status : str
    gate_type : str
    airport_id : UUID
    created_at : datetime
    updated_at : datetime
    class Config:
        from_attributes = True

class GateUpdate(BaseModel):
    gate_code : Optional[str] = None
    terminal : Optional[str] = None
    status : Optional[str] = None
    gate_type : Optional[str] = None
    airport_id : Optional[str] = None
