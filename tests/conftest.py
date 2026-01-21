import pytest
import sys
from pathlib import Path

# FORCER le PYTHONPATH
sys.path.insert(0, str(Path(__file__).parent.parent))

from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from fastapi.testclient import TestClient

# Base de données en MÉMOIRE pour les tests
TEST_DATABASE_URL = "sqlite:///:memory:"

@pytest.fixture
def api_url():
    return "http://localhost:8000/api/v1"

@pytest.fixture(scope="function")
def db_session():
    """Session isolée avec rollback automatique"""
    from app.core.database import Base
    import app.models.airport
    import app.models.runway
    import app.models.gate
    import app.models.flight
    import app.models.slot
    
    # Créer engine EN MÉMOIRE (disparaît après chaque test)
    engine = create_engine(
        TEST_DATABASE_URL,
        connect_args={"check_same_thread": False}  # Important pour SQLite
    )
    
    # Créer TOUTES les tables
    Base.metadata.create_all(bind=engine)
    
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
    
    # ROLLBACK automatique - annule TOUS les changements
    session.close()
    transaction.rollback()
    connection.close()
    
    # Supprimer toutes les tables
    Base.metadata.drop_all(bind=engine)
    engine.dispose()

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
