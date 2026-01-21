import pytest
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).parent.parent))

from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from fastapi.testclient import TestClient

@pytest.fixture
def api_url():
    return "http://localhost:8000/api/v1"

@pytest.fixture(scope="function")
def client():
    """Client FastAPI avec DB en mémoire isolée"""
    # Import Base et modèles
    from app.core.database import Base, get_db
    from app.main import app
    from app.models import airport, runway, gate, flight, slot
    
    # Créer engine en mémoire
    engine = create_engine(
        "sqlite:///:memory:",
        connect_args={"check_same_thread": False}
    )
    
    # CRÉER TOUTES LES TABLES
    Base.metadata.create_all(bind=engine)
    
    # Créer SessionLocal
    TestingSessionLocal = sessionmaker(
        autocommit=False,
        autoflush=False,
        bind=engine
    )
    
    # Override get_db
    def override_get_db():
        db = TestingSessionLocal()
        try:
            yield db
        finally:
            db.close()
    
    app.dependency_overrides[get_db] = override_get_db
    
    # Créer le client
    with TestClient(app) as test_client:
        yield test_client
    
    # Cleanup
    app.dependency_overrides.clear()
    Base.metadata.drop_all(bind=engine)
    engine.dispose()

@pytest.fixture(scope="function")
def db_session():
    """Session pour tests directs (sans FastAPI)"""
    from app.core.database import Base
    from app.models import airport, runway, gate, flight, slot
    
    engine = create_engine(
        "sqlite:///:memory:",
        connect_args={"check_same_thread": False}
    )
    
    Base.metadata.create_all(bind=engine)
    
    Session = sessionmaker(bind=engine)
    session = Session()
    
    yield session
    
    session.close()
    Base.metadata.drop_all(bind=engine)
    engine.dispose()
