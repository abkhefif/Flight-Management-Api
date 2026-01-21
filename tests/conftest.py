import pytest
import sys
from pathlib import Path
import os

# FORCER le PYTHONPATH
sys.path.insert(0, str(Path(__file__).parent.parent))

from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from fastapi.testclient import TestClient

# Chemin vers la DB de test
TEST_DATABASE_URL = "sqlite:///./test.db"

@pytest.fixture
def api_url():
    return "http://localhost:8000/api/v1"

@pytest.fixture(scope="session", autouse=True)
def setup_test_database():
    """Crée la DB de test au début de la session, la supprime à la fin"""
    # Import tous les modèles
    from app.core.database import Base
    import app.models.airport
    import app.models.runway
    import app.models.gate
    import app.models.flight
    import app.models.slot
    
    # Créer l'engine
    engine = create_engine(TEST_DATABASE_URL)
    
    # Créer toutes les tables
    Base.metadata.create_all(bind=engine)
    
    yield
    
    # Cleanup : supprimer la DB de test
    engine.dispose()
    if os.path.exists("./test.db"):
        os.remove("./test.db")

@pytest.fixture(scope="function")
def db_session():
    """Session avec transaction + rollback automatique"""
    from app.core.database import Base
    
    # Créer engine
    engine = create_engine(TEST_DATABASE_URL)
    
    # Créer une connexion
    connection = engine.connect()
    
    # Commencer une transaction
    transaction = connection.begin()
    
    # Créer une session liée à cette transaction
    TestingSessionLocal = sessionmaker(
        autocommit=False,
        autoflush=False,
        bind=connection
    )
    session = TestingSessionLocal()
    
    yield session
    
    # Rollback la transaction (annule TOUS les changements)
    session.close()
    transaction.rollback()
    connection.close()

@pytest.fixture(scope="function")
def client(db_session):
    """Client FastAPI avec DB override"""
    from app.main import app
    from app.core.database import get_db
    
    def override_get_db():
        try:
            yield db_session
        finally:
            pass
    
    app.dependency_overrides[get_db] = override_get_db
    
    with TestClient(app) as test_client:
        yield test_client
    
    app.dependency_overrides.clear()
