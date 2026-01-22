"""
Configuration de test pour Flight Management System
Utilise une base de données SQLite en mémoire isolée pour chaque test.
"""
import pytest
import os
import sys
from pathlib import Path

# Ajouter le chemin racine
sys.path.insert(0, str(Path(__file__).parent.parent))

from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from sqlalchemy.pool import StaticPool
from fastapi.testclient import TestClient


@pytest.fixture
def api_url():
    """URL de base pour l'API"""
    return "/api/v1"


@pytest.fixture(scope="function")
def client():
    """
    Client FastAPI avec DB SQLite en mémoire.
    Chaque test obtient une DB fraîche et isolée.
    """
    # Créer un engine SQLite en mémoire avec StaticPool pour partager la connexion
    # entre les threads (nécessaire pour FastAPI + SQLite en mémoire)
    test_engine = create_engine(
        "sqlite:///:memory:",
        connect_args={"check_same_thread": False},
        poolclass=StaticPool,  # Crucial pour SQLite en mémoire avec FastAPI
    )
    
    TestingSessionLocal = sessionmaker(
        autocommit=False,
        autoflush=False,
        bind=test_engine
    )
    
    # Importer Base et les modèles pour créer les tables
    from app.core.database import Base
    from app.models import Airport, Runway, Gate, Flight, Slot
    
    # Créer toutes les tables dans la DB de test
    Base.metadata.create_all(bind=test_engine)
    
    # Importer l'app et la fonction get_db
    from app.main import app
    from app.core.database import get_db
    
    # Fonction override pour injecter notre session de test
    def override_get_db():
        db = TestingSessionLocal()
        try:
            yield db
        finally:
            db.close()
    
    # Appliquer l'override
    app.dependency_overrides[get_db] = override_get_db
    
    # Créer et retourner le client de test
    with TestClient(app) as test_client:
        yield test_client
    
    # Cleanup après le test
    app.dependency_overrides.clear()
    Base.metadata.drop_all(bind=test_engine)
    test_engine.dispose()


@pytest.fixture(scope="function")
def db_session():
    """
    Session de base de données pour tests directs sans FastAPI.
    Utile pour tester les modèles et services directement.
    """
    from app.core.database import Base
    from app.models import Airport, Runway, Gate, Flight, Slot
    
    test_engine = create_engine(
        "sqlite:///:memory:",
        connect_args={"check_same_thread": False},
        poolclass=StaticPool,
    )
    
    Base.metadata.create_all(bind=test_engine)
    
    TestingSessionLocal = sessionmaker(bind=test_engine)
    session = TestingSessionLocal()
    
    yield session
    
    session.close()
    Base.metadata.drop_all(bind=test_engine)
    test_engine.dispose()
