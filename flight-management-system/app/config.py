"""Configuration de l'application"""
from pydantic_settings import BaseSettings


class Settings(BaseSettings):
    """Settings chargés depuis .env"""
    PROJECT_NAME: str = "Flight Management System"
    API_V1_PREFIX: str = "/api/v1"
    DATABASE_URL: str = "sqlite:///./fms.db"
    ENVIRONMENT: str = "development"
    
    class Config:
        env_file = ".env"


settings = Settings()
