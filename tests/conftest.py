import pytest
import requests
from sqlalchemy import create_engine
from app.core.database import SessionLocal
from sqlalchemy.orm import sessionmaker
from app.core.database import Base
from fastapi.testclient import TestClient

#fixture = Fonction qui prepare des donnees reutilisables
@pytest.fixture
def api_url():
    return ("http://localhost:8000/api/v1")
@pytest.fixture
def client(db_session):
    from fastapi.testclient import TestClient
    from app.main import app
    from app.core.database import get_db
    def override_get_db():
        try:
            yield db_session
        finally:
            pass
    app.dependency_overrides[get_db] = override_get_db
    # Créer le client (sans context manager)
    test_client = TestClient(app)
    yield test_client
    test_client.close()
    # Cleanup
    app.dependency_overrides.clear()
@pytest.fixture
def db_session():
    engine = create_engine("sqlite:///:memory:")
    # engine dit ou est la DB, ici sur memoire ram, pour les tests
    Base.metadata.create_all(engine)
    SessionLocal = sessionmaker(bind=engine)
    # build les tables necessaire (airports,runways, etc..)
    session = SessionLocal()
    yield session
    session.close()
