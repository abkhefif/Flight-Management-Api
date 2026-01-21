from pydantic import BaseModel
from uuid import UUID
from datetime import datetime
from typing import Optional
from pydantic import BaseModel, validator
# Schema CREATE

class FlightCreate(BaseModel):
    flight_number: str
    airline: str
    departure_airport_id: UUID
    arrival_airport_id: UUID
    departure_gate_id: Optional[UUID] = None
    arrival_gate_id: Optional[UUID] = None
    scheduled_departure: datetime
    scheduled_arrival: datetime
    actual_departure: Optional[datetime] = None
    actual_arrival: Optional[datetime] = None
    status: str

    @validator('arrival_airport_id')
    def airport_must_be_diff(cls, v, values):
        departure_id = values.get('departure_airport_id')
        if v == departure_id:
            raise ValueError('Departure and arrival airports must be different')
        return v

    @validator('scheduled_arrival')
    def arrival_after_departure_min_15_min(cls, v, values):
        scheduled_departure = values.get('scheduled_departure')
        if not scheduled_departure:
            return v
        if v <= scheduled_departure:
            raise ValueError('Arrival must be after departure')
        duration_minutes = (v - scheduled_departure).total_seconds() / 60
        if duration_minutes < 15:
            raise ValueError('Flight duration must be at least 15 minutes')
        return v

class FlightRead(BaseModel):
    id: UUID
    flight_number: str
    airline: str
    departure_airport_id: UUID
    arrival_airport_id: UUID
    departure_gate_id: Optional[UUID] = None
    arrival_gate_id: Optional[UUID] = None
    scheduled_departure: datetime
    scheduled_arrival: datetime
    actual_departure: Optional[datetime] = None
    actual_arrival: Optional[datetime] = None
    status: str
    created_at: datetime
    updated_at: datetime
    
    class Config:
        from_attributes = True

class FlightUpdate(BaseModel):
    flight_number: Optional[str] = None
    airline: Optional[str] = None
    departure_airport_id: Optional[UUID] = None
    arrival_airport_id: Optional[UUID] = None
    departure_gate_id: Optional[UUID] = None
    arrival_gate_id: Optional[UUID] = None
    scheduled_departure: Optional[datetime] = None
    scheduled_arrival: Optional[datetime] = None
    actual_departure: Optional[datetime] = None
    actual_arrival: Optional[datetime] = None
    status: Optional[str] = None
