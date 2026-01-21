import pytest
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).parent.parent))

from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from fastapi.testclient import TestClient

TEST_DATABASE_URL = "sqlite:///:memory:"

@pytest.fixture
def api_url():
    return "http://localhost:8000/api/v1"

@pytest.fixture(scope="function")
def test_engine():
    """Créer un engine de test avec les tables"""
    # Import Base et TOUS les modèles
    from app.core.database import Base
    from app.models import airport, runway, gate, flight, slot
    
    engine = create_engine(
        TEST_DATABASE_URL,
        connect_args={"check_same_thread": False}
    )
    
    # CRÉER LES TABLES ICI
    Base.metadata.create_all(bind=engine)
    
    yield engine
    
    # Cleanup
    Base.metadata.drop_all(bind=engine)
    engine.dispose()

@pytest.fixture(scope="function")
def db_session(test_engine):
    """Session avec rollback automatique"""
    connection = test_engine.connect()
    transaction = connection.begin()
    
    Session = sessionmaker(
        autocommit=False,
        autoflush=False,
        bind=connection
    )
    session = Session()
    
    yield session
    
    session.close()
    transaction.rollback()
    connection.close()

@pytest.fixture(scope="function")
def client(test_engine):
    """Client FastAPI avec DB test"""
    from app.main import app
    from app.core.database import get_db
    
    # Créer une SessionLocal qui utilise test_engine
    TestingSessionLocal = sessionmaker(
        autocommit=False,
        autoflush=False,
        bind=test_engine
    )
    
    def override_get_db():
        db = TestingSessionLocal()
        try:
            yield db
        finally:
            db.close()
    
    app.dependency_overrides[get_db] = override_get_db
    
    with TestClient(app) as c:
        yield c
    
    app.dependency_overrides.clear()
