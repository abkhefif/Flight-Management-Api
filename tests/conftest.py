import pytest
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from fastapi.testclient import TestClient

@pytest.fixture
def api_url():
    return "http://localhost:8000/api/v1"

@pytest.fixture(scope="session")
def test_engine():
    """Crée un engine SQLite en mémoire pour tous les tests"""
    # IMPORTANT: Importer Base et TOUS les modèles AVANT create_all
    from app.core.database import Base
    from app.models.airport import Airport
    from app.models.runway import Runway
    from app.models.gate import Gate
    from app.models.flight import Flight
    from app.models.slot import Slot
    
    engine = create_engine("sqlite:///:memory:")
    Base.metadata.create_all(engine)
    yield engine
    engine.dispose()

@pytest.fixture(scope="function")
def db_session(test_engine):
    """Crée une nouvelle session DB pour chaque test avec rollback automatique"""
    connection = test_engine.connect()
    transaction = connection.begin()
    
    SessionLocal = sessionmaker(bind=connection)
    session = SessionLocal()
    
    yield session
    
    session.close()
    transaction.rollback()
    connection.close()

@pytest.fixture(scope="function")
def client(db_session):
    """Crée un TestClient FastAPI avec override de la DB"""
    from app.main import app
    from app.core.database import get_db
    
    def override_get_db():
        try:
            yield db_session
        finally:
            pass
    
    app.dependency_overrides[get_db] = override_get_db
    
    test_client = TestClient(app)
    yield test_client
    test_client.close()
    
    app.dependency_overrides.clear()
