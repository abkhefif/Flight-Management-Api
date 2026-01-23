from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session
from typing import List

from app.core.database import SessionLocal
from app.schemas.airport import AirportRead
from app.models.airport import Airport
from app.schemas.airport import AirportUpdate
from app.schemas.airport import AirportCreate

from fastapi import APIRouter, Depends, FastAPI, HTTPException
from fastapi.security import HTTPBasic, HTTPBasicCredentials
from sqlalchemy.orm import Session
from fastapi.openapi.docs import get_swagger_ui_html
from typing import List
from app.core.auth import verify_credentials

from app.core.database import SessionLocal
from app.schemas.airport import AirportRead
from app.models.airport import Airport
from app.models.runway import Runway
from app.models.gate import Gate
from app.models.slot import Slot
from app.models.flight import Flight
from fastapi import FastAPI
from slowapi import Limiter, _rate_limit_exceeded_handler
from slowapi.util import get_remote_address
from slowapi.errors import RateLimitExceeded
from slowapi.middleware import SlowAPIMiddleware

from app.api.v1.routes.airports import router as airports_router
from app.api.v1.routes.runways import router as runways_router
from app.api.v1.routes.gates import router as gates_router
from app.api.v1.routes.slots import router as slots_router
from app.api.v1.routes.flights import router as flights_router

limiter = Limiter(key_func = get_remote_address, default_limits=["100/minute"])
# cree le limiter de request par ip , de 100 / minute p1 = ip , p2 = limite

app = FastAPI(
        title = "Flight Management System API",
        description = "API for managing airports, flights, runways, gates, and slots",
        version = "1.0.0",
        docs_url = None,
        redoc_url = None
        )

app.state.limiter = limiter
app.add_exception_handler(RateLimitExceeded, _rate_limit_exceeded_handler)
app.add_middleware(SlowAPIMiddleware)
#app.state = espace de stockage Fastapi, pour mettre des objets customs

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

@app.get("/health")
def health_check():
    return {"status": "healthy"}

@app.get("/docs", include_in_schema = False)
def custom_swagger_ui(credentials: HTTPBasicCredentials = Depends(verify_credentials)):
    return get_swagger_ui_html(
        openapi_url="/openapi.json",
        title="Flight Management System - Docs"
    )
