from pydantic import BaseModel, ConfigDict, Field, validator
from typing import Optional
from uuid import UUID
from datetime import datetime

class AirportCreate(BaseModel):
    code: str
    name: str
    city: str
    country: str
    timezone: str

class AirportRead(BaseModel):
    id: UUID
    code: str
    name: str
    city: str
    country: str
    timezone: str
    created_at: datetime
    updated_at: datetime 
    class Config:
        from_attributes = True
class AirportUpdate(BaseModel):
    code: Optional[str] = None
    name: Optional[str] = None
    city: Optional[str] = None
    country: Optional[str] = None
    timezone: Optional[str] = None
