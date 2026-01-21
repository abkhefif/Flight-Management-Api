from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session
from typing import List

from app.core.database import SessionLocal
from app.schemas.airport import AirportRead
from app.models.airport import Airport
from app.schemas.airport import AirportUpdate
from app.schemas.airport import AirportCreate

from fastapi import APIRouter, Depends, FastAPI, HTTPException
from sqlalchemy.orm import Session
from typing import List

from app.core.database import SessionLocal
from app.schemas.airport import AirportRead
from app.models.airport import Airport
from app.models.runway import Runway
from app.models.gate import Gate
from app.models.slot import Slot
from app.models.flight import Flight
from fastapi import FastAPI

from app.api.v1.routes.airports import router as airports_router
from app.api.v1.routes.runways import router as runways_router
from app.api.v1.routes.gates import router as gates_router
from app.api.v1.routes.slots import router as slots_router
from app.api.v1.routes.flights import router as flights_router

app = FastAPI(
        title = "Flight Management System API",
        description = "API for managing airports, flights, runways, gates, and slots",
        version = "1.0.0"
        )

app.include_router(
        airports_router,
        prefix="/api/v1/airports",
        tags=["Airports"]
        )

app.include_router(
        runways_router,
        prefix="/api/v1/runways",
        tags=["Runways"]
        )

app.include_router(
        gates_router,
        prefix="/api/v1/gates",
        tags=["Gates"]
        )

app.include_router(
        slots_router,
        prefix="/api/v1/slots",
        tags=["Slots"]
        )

app.include_router(
        flights_router,
        prefix="/api/v1/flights",
        tags=["Flights"]
        )

@app.get("/")
def root():
    return {
        "message" : "Welcome to Flight Management System API",
        "version" : "1.0.0",
        "docs" : "/docs"
    }
