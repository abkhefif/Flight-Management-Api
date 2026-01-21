from app.models.airport import Airport
from app.models.runway import Runway
from app.models.gate import Gate
from app.models.slot import Slot
from app.models.flight import Flight

def test_db_session_create_airport(db_session):
    airport = Airport(
            id="test-123",
            code="TST",
            name="Test Airport",
            city="Test City",
            country="Test Country",
            timezone="UTC"
            )
    db_session.add(airport)
    db_session.commit()
    result = db_session.query(Airport).filter(Airport.id == "test-123").first()
    assert result is not None
#    for key in airport:
#        assert aiport[key] == result[key]
    assert result.id == airport.id
    assert result.code == airport.code
    assert result.name == airport.name
    assert result.city == airport.city
    assert result.country == airport.country
    assert result.timezone == airport.timezone
