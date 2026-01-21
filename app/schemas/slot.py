from pydantic import BaseModel
from uuid import UUID
from datetime import datetime
from typing import Optional
from pydantic import BaseModel, validator

class SlotCreate(BaseModel):
    slot_type: str         
    start_time: datetime
    end_time: datetime
    status: str
    airport_id: UUID
    runway_id: UUID
    flight_id: Optional[UUID] = None

    @validator('end_time')
    def end_after_start(cls, v, values):
        start_time = values.get('start_time')
        if v <= start_time:
            raise ValueError('End must be after start')
        duration_minutes = (v - start_time).total_seconds() / 60
        if duration_minutes < 15:
            raise ValueError('Slot reservation must be at least 15 minutes')
        if duration_minutes > 60:
            raise ValueError('Slot reservation cannot exceed 60 minutes')
        return v

class SlotRead(BaseModel):
    id: UUID
    slot_type: str
    start_time: datetime
    end_time: datetime
    status: str
    airport_id: UUID
    runway_id: UUID
    flight_id: Optional[UUID] = None
    created_at: datetime
    updated_at: datetime
    
    class Config:
        from_attributes = True

class SlotUpdate(BaseModel):
    slot_type: Optional[str] = None
    start_time: Optional[datetime] = None
    end_time: Optional[datetime] = None
    status: Optional[str] = None
    airport_id: Optional[UUID] = None
    runway_id: Optional[UUID] = None
    flight_id: Optional[UUID] = None
