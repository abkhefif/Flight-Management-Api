import pytest
import sys
from pathlib import Path

# FORCER le PYTHONPATH (au cas où)
sys.path.insert(0, str(Path(__file__).parent.parent))

from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from fastapi.testclient import TestClient

@pytest.fixture
def api_url():
    return "http://localhost:8000/api/v1"

@pytest.fixture(scope="function")
def db_session():
    """Recrée la DB pour CHAQUE test - 100% isolé"""
    # Import TOUS les modèles explicitement
    from app.core.database import Base
    import app.models.airport
    import app.models.runway
    import app.models.gate
    import app.models.flight
    import app.models.slot
    
    # Créer engine SQLITE en mémoire
    engine = create_engine(
        "sqlite:///:memory:",
        connect_args={"check_same_thread": False}
    )
    
    # Créer TOUTES les tables
    Base.metadata.create_all(bind=engine)
    
    # Créer session
    TestingSessionLocal = sessionmaker(
        autocommit=False,
        autoflush=False,
        bind=engine
    )
    session = TestingSessionLocal()
    
    yield session
    
    # Cleanup
    session.close()
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
    
    # Override la dépendance
    app.dependency_overrides[get_db] = override_get_db
    
    # Créer le client
    with TestClient(app) as test_client:
        yield test_client
    
    # Cleanup
    app.dependency_overrides.clear()
