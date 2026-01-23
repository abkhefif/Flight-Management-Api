import random
from uuid import uuid4
import uuid
from datetime import datetime, timedelta

def test_lists_airports(client, api_url):
    #GET /api_url/airports
    response = client.get(f"{api_url}/airports")
    data = response.json()
    assert response.status_code == 200
    assert isinstance(data, list)

def test_create_airports(client, api_url):
    code = f"TEST{str(uuid.uuid4())[:8].upper()}"

    airport_data = {
            "code": code,
            "name": "Test Airport",
            "city": "Test City",
            "country": "Test Country",
            "timezone": "UTC"
                    }
    response = client.post(f"{api_url}/airports",json = airport_data)
    print(f"\nStatus: {response.status_code}")
    print(f"Text: {response.text}")
    print(f"Headers: {response.headers}\n")
    data = response.json()
    assert response.status_code == 201
    
    assert data["code"] == code
    assert data["name"] == "Test Airport"
    assert data["city"] == "Test City"
    assert data["country"] == "Test Country"
    assert data["timezone"] == "UTC"

def test_update_airport(client, api_url):
    code = f"TEST{str(uuid.uuid4())[:8].upper()}"

    airport_data = {
            "code": code,
            "name": "Test Airport",
            "city": "Test City",
            "country": "Test Country",
            "timezone": "UTC"
                    }
    response = client.post(f"{api_url}/airports",json = airport_data)
    print(f"\nStatus: {response.status_code}")
    print(f"Text: {response.text}")
    print(f"Headers: {response.headers}\n")
    data = response.json()
    assert response.status_code == 201

    airport_update = {
            "code" : code,
            "name" : "test_update_name",
            "city" : "test_update_city",
            "country" : "test_update_country",
            "timezone" : "test_update_timezone"
            }

    airport_id = data["id"]
    response_update = client.put(f"{api_url}/airports/{airport_id}", json = airport_update)
    assert response_update.status_code == 200
    data_update = response_update.json()

    assert data_update["code"] == code
    assert data_update["name"] == "test_update_name"
    assert data_update["city"] == "test_update_city"
    assert data_update["country"] == "test_update_country"
    assert data_update["timezone"] == "test_update_timezone"

def test_delete_airport(client, api_url):
    code = f"TEST{str(uuid.uuid4())[:8].upper()}"

    airport_data = {
            "code": code,
            "name": "Test Airport",
            "city": "Test City",
            "country": "Test Country",
            "timezone": "UTC"
                    }
    response = client.post(f"{api_url}/airports",json = airport_data)
    print(f"\nStatus: {response.status_code}")
    print(f"Text: {response.text}")
    print(f"Headers: {response.headers}\n")
    data = response.json()
    assert response.status_code == 201

    airport_update = {
            "code" : code,
            "name" : "test_update_name",
            "city" : "test_update_city",
            "country" : "test_update_country",
            "timezone" : "test_update_timezone"
            }

    airport_id = data["id"]
    response_update = client.delete(f"{api_url}/airports/{airport_id}")
    assert response_update.status_code == 200

# Test negatifs :

def test_get_airport_not_found(client, api_url):
    fake_id = "00000000-0000-0000-0000-000000000000"
    response = client.get(f"{api_url}/airports/{fake_id}")
    assert response.status_code == 404
    #assert response.json()["detail"] == "Airport not found"


def test_update_airport_not_found(client, api_url):
    fake_id = "00000000-0000-0000-0000-000000000000"
    flight_update = {"origin": "XXX", "destination": "YYY"}
    response = client.put(f"{api_url}/airports/{fake_id}", json=flight_update)
    assert response.status_code == 404
    assert response.json()["detail"] == "Airport not found"


def test_delete_airport_not_found(client, api_url):
    fake_id = "00000000-0000-0000-0000-000000000000"
    response = client.delete(f"{api_url}/airports/{fake_id}")
    assert response.status_code == 404
    assert response.json()["detail"] == "Airport not found"

#def test_list_flights_empty(client, api_url):
    response = client.get(f"{api_url}/airport")
    assert response.status_code == 200
    assert response.json() == []

#def test_update_flight_uuid_field(client, api_url):
    flight_data = {
        "flight_number": "AF999",
        "airline": "Air France",
        "departure_airport_id": str(uuid4()),
        "arrival_airport_id": str(uuid4()),
        "scheduled_departure": datetime.utcnow().isoformat(),
        "scheduled_arrival": (datetime.utcnow() + timedelta(hours=2)).isoformat(),
        "status": "scheduled"
    }

    response = client.post(f"{api_url}/flights", json=flight_data)

    print(response.status_code, response.text)

    assert response.status_code == 201
    flight_id = response.json()["id"]

    new_airport_id = str(uuid4())

    response = client.put(
        f"{api_url}/flights/{flight_id}",
        json={"departure_airport_id": new_airport_id}
    )

    assert response.status_code == 200

def test_delete_airport_not_found(client, api_url):
    fake_id = "00000000-0000-0000-0000-000000000000"
    response = client.delete(f"{api_url}/airports/{fake_id}")
    assert response.status_code == 404

