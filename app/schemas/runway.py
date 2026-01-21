from pydantic import BaseModel, ConfigDict
from typing import Optional
from uuid import UUID
from datetime import datetime

class RunwayCreate(BaseModel):
    runway_code : str
    length_meters : int
    width_meters : int
    surface_type : str
    status : str
    airport_id : str

class RunwayRead(BaseModel):
    id : UUID
    runway_code : str
    length_meters : int
    width_meters : int
    surface_type : str
    status : str
    airport_id : UUID
    created_at : datetime
    updated_at : datetime
    class Config:
        from_attributes = True

class RunwayUpdate(BaseModel):
    runway_code : Optional[str] = None
    length_meters : Optional[int] = None
    width_meters : Optional[int] = None
    surface_type : Optional[str] = None
    status : Optional[str] = None
    airport_id : Optional[str] = None
