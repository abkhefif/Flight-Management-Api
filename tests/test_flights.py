import random
from uuid import uuid4
from datetime import datetime, timedelta
import uuid

def test_create_flight_basic(client, api_url):
    airport_1 = {
            "code" : f"TEST{str(uuid.uuid4())[:8].upper()}",
            "name" : "Departue Airport",
            "city" : "Testcity",
            "country" : "Testcountry",
            "timezone" : "Testzone"
            }
    airport_2 = {
            "code" : f"TEST{str(uuid.uuid4())[:8].upper()}",
            "name" : "Arrival Airport",
            "city" : "Testcity2",
            "country" : "Testcountry2",
            "timezone" : "Testzone2"
            }

    response_dep_airport = client.post(f"{api_url}/airports", json = airport_1)
    assert response_dep_airport.status_code == 201
    depart_airport = response_dep_airport.json()

    response_ariv_airport = client.post(f"{api_url}/airports", json = airport_2)
    assert response_ariv_airport.status_code == 201
    ariv_airport = response_ariv_airport.json()

    runway_1 = {
            "runway_code" : "Testrunway_1",
            "length_meters" : 123,
            "width_meters" : 321,
            "surface_type" : "asphalt",
            "status" : "AVAILABLE",
            "airport_id" : depart_airport["id"]
            }
    runway_2 = {
            "runway_code" : "Testrunway_2",
            "length_meters" : 321,
            "width_meters" : 123,
            "surface_type" : "asphalt",
            "status" : "AVAILABLE",
            "airport_id" : ariv_airport["id"]
            }
    dep_runway_resp = client.post(f"{api_url}/runways", json = runway_1)
    assert dep_runway_resp.status_code == 201
    dep_runway = dep_runway_resp.json()
    assert dep_runway["runway_code"] == "Testrunway_1"
    assert dep_runway["airport_id"] == depart_airport["id"]

    ariv_runway_resp = client.post(f"{api_url}/runways", json = runway_2)
    assert ariv_runway_resp.status_code == 201
    ariv_runway = ariv_runway_resp.json()
    assert ariv_runway["runway_code"] == "Testrunway_2"
    assert ariv_runway["airport_id"] == ariv_airport["id"]
    
    gate_1 = {
            "gate_code" : "Gate_test1",
            "terminal" : "Terminal_test_1",
            "status" : "Test_status",
            "gate_type" : "Test_gate_type",
            "airport_id" : depart_airport["id"]
            }
    gate_2 = {
            "gate_code" : "Gate_test1",
            "terminal" : "Terminal_test_2",
            "status" : "Test_status",
            "gate_type" : "Test_gate_type",
            "airport_id" : depart_airport["id"]
            }
    dep_gate_resp = client.post(f"{api_url}/gates", json = gate_1)
    assert dep_gate_resp.status_code == 201
    dep_gate = dep_gate_resp.json()
    assert dep_gate["airport_id"] == depart_airport["id"]
    assert dep_gate["gate_code"] == "Gate_test1"
    dep_gate_resp = client.post(f"{api_url}/gates", json = gate_1)
    ariv_gate_resp = client.post(f"{api_url}/gates", json = gate_1)
    assert ariv_gate_resp.status_code == 201
    ariv_gate = ariv_gate_resp.json()
    assert ariv_gate["airport_id"] == depart_airport["id"]
    assert ariv_gate["gate_code"] == "Gate_test1"
    
    now = datetime.utcnow()

    flight_1 = {
            "flight_number": f"TEST{str(uuid.uuid4())[:8].upper()}",
            "airline" : "AF987",
            "departure_airport_id" : depart_airport["id"],
            "arrival_airport_id" : ariv_airport["id"],
            "scheduled_departure": (now + timedelta(hours=2)).isoformat(),
            "scheduled_arrival": (now + timedelta(hours=5)).isoformat(),
            "status" : "SCHEDULED"
            }
    response_flight = client.post(f"{api_url}/flights", json = flight_1)
    print(response_flight.json())
    assert response_flight.status_code == 201
    flight = response_flight.json()

def test_delete_flight_basic(client, api_url):
    airport_1 = {
            "code" : f"TEST{str(uuid.uuid4())[:8].upper()}",
            "name" : "Departue Airport",
            "city" : "Testcity",
            "country" : "Testcountry",
            "timezone" : "Testzone"
            }
    airport_2 = {
            "code" : f"TEST{str(uuid.uuid4())[:8].upper()}",
            "name" : "Arrival Airport",
            "city" : "Testcity2",
            "country" : "Testcountry2",
            "timezone" : "Testzone2"
            }

    response_dep_airport = client.post(f"{api_url}/airports", json = airport_1)
    assert response_dep_airport.status_code == 201
    depart_airport = response_dep_airport.json()

    response_ariv_airport = client.post(f"{api_url}/airports", json = airport_2)
    assert response_ariv_airport.status_code == 201
    ariv_airport = response_ariv_airport.json()

    runway_1 = {
            "runway_code" : "Testrunway_1",
            "length_meters" : 123,
            "width_meters" : 321,
            "surface_type" : "asphalt",
            "status" : "AVAILABLE",
            "airport_id" : depart_airport["id"]
            }
    runway_2 = {
            "runway_code" : "Testrunway_2",
            "length_meters" : 321,
            "width_meters" : 123,
            "surface_type" : "asphalt",
            "status" : "AVAILABLE",
            "airport_id" : ariv_airport["id"]
            }
    dep_runway_resp = client.post(f"{api_url}/runways", json = runway_1)
    assert dep_runway_resp.status_code == 201
    dep_runway = dep_runway_resp.json()
    assert dep_runway["runway_code"] == "Testrunway_1"
    assert dep_runway["airport_id"] == depart_airport["id"]

    ariv_runway_resp = client.post(f"{api_url}/runways", json = runway_2)
    assert ariv_runway_resp.status_code == 201
    ariv_runway = ariv_runway_resp.json()
    assert ariv_runway["runway_code"] == "Testrunway_2"
    assert ariv_runway["airport_id"] == ariv_airport["id"]

    gate_1 = {
            "gate_code" : "Gate_test1",
            "terminal" : "Terminal_test_1",
            "status" : "Test_status",
            "gate_type" : "Test_gate_type",
            "airport_id" : depart_airport["id"]
            }
    gate_2 = {
            "gate_code" : "Gate_test1",
            "terminal" : "Terminal_test_2",
            "status" : "Test_status",
            "gate_type" : "Test_gate_type",
            "airport_id" : depart_airport["id"]
            }
    dep_gate_resp = client.post(f"{api_url}/gates", json = gate_1)
    assert dep_gate_resp.status_code == 201
    dep_gate = dep_gate_resp.json()
    assert dep_gate["airport_id"] == depart_airport["id"]
    assert dep_gate["gate_code"] == "Gate_test1"
    dep_gate_resp = client.post(f"{api_url}/gates", json = gate_1)
    ariv_gate_resp = client.post(f"{api_url}/gates", json = gate_1)
    assert ariv_gate_resp.status_code == 201
    ariv_gate = ariv_gate_resp.json()
    assert ariv_gate["airport_id"] == depart_airport["id"]
    assert ariv_gate["gate_code"] == "Gate_test1"

    now = datetime.utcnow()

    flight_1 = {
            "flight_number": f"TEST{str(uuid.uuid4())[:8].upper()}",
            "airline" : "AF987",
            "departure_airport_id" : depart_airport["id"],
            "arrival_airport_id" : ariv_airport["id"],
            "scheduled_departure": (now + timedelta(hours=2)).isoformat(),
            "scheduled_arrival": (now + timedelta(hours=5)).isoformat(),
            "status" : "SCHEDULED"
            }
    response_flight = client.post(f"{api_url}/flights", json = flight_1)
    print(response_flight.json())
    assert response_flight.status_code == 201
    flight = response_flight.json()
    flight_id = flight["id"]
    response_update = client.delete(f"{api_url}/flights/{flight_id}")
    assert response_update.status_code == 200

def test_update_flight_basic(client, api_url):
    airport_1 = {
            "code" : f"TEST{str(uuid.uuid4())[:8].upper()}",
            "name" : "Departue Airport",
            "city" : "Testcity",
            "country" : "Testcountry",
            "timezone" : "Testzone"
            }
    airport_2 = {
            "code" : f"TEST{str(uuid.uuid4())[:8].upper()}",
            "name" : "Arrival Airport",
            "city" : "Testcity2",
            "country" : "Testcountry2",
            "timezone" : "Testzone2"
            }

    response_dep_airport = client.post(f"{api_url}/airports", json = airport_1)
    assert response_dep_airport.status_code == 201
    depart_airport = response_dep_airport.json()

    response_ariv_airport = client.post(f"{api_url}/airports", json = airport_2)
    assert response_ariv_airport.status_code == 201
    ariv_airport = response_ariv_airport.json()

    runway_1 = {
            "runway_code" : "Testrunway_1",
            "length_meters" : 123,
            "width_meters" : 321,
            "surface_type" : "asphalt",
            "status" : "AVAILABLE",
            "airport_id" : depart_airport["id"]
            }
    runway_2 = {
            "runway_code" : "Testrunway_2",
            "length_meters" : 321,
            "width_meters" : 123,
            "surface_type" : "asphalt",
            "status" : "AVAILABLE",
            "airport_id" : ariv_airport["id"]
            }
    dep_runway_resp = client.post(f"{api_url}/runways", json = runway_1)
    assert dep_runway_resp.status_code == 201
    dep_runway = dep_runway_resp.json()
    assert dep_runway["runway_code"] == "Testrunway_1"
    assert dep_runway["airport_id"] == depart_airport["id"]

    ariv_runway_resp = client.post(f"{api_url}/runways", json = runway_2)
    assert ariv_runway_resp.status_code == 201
    ariv_runway = ariv_runway_resp.json()
    assert ariv_runway["runway_code"] == "Testrunway_2"
    assert ariv_runway["airport_id"] == ariv_airport["id"]

    gate_1 = {
            "gate_code" : "Gate_test1",
            "terminal" : "Terminal_test_1",
            "status" : "Test_status",
            "gate_type" : "Test_gate_type",
            "airport_id" : depart_airport["id"]
            }
    gate_2 = {
            "gate_code" : "Gate_test1",
            "terminal" : "Terminal_test_2",
            "status" : "Test_status",
            "gate_type" : "Test_gate_type",
            "airport_id" : depart_airport["id"]
            }
    dep_gate_resp = client.post(f"{api_url}/gates", json = gate_1)
    assert dep_gate_resp.status_code == 201
    dep_gate = dep_gate_resp.json()
    assert dep_gate["airport_id"] == depart_airport["id"]
    assert dep_gate["gate_code"] == "Gate_test1"
    dep_gate_resp = client.post(f"{api_url}/gates", json = gate_1)
    ariv_gate_resp = client.post(f"{api_url}/gates", json = gate_1)
    assert ariv_gate_resp.status_code == 201
    ariv_gate = ariv_gate_resp.json()
    assert ariv_gate["airport_id"] == depart_airport["id"]
    assert ariv_gate["gate_code"] == "Gate_test1"

    now = datetime.utcnow()

    flight_1 = {
            "flight_number": f"TEST{str(uuid.uuid4())[:8].upper()}",
            "airline" : "AF987",
            "departure_airport_id" : depart_airport["id"],
            "arrival_airport_id" : ariv_airport["id"],
            "scheduled_departure": (now + timedelta(hours=2)).isoformat(),
            "scheduled_arrival": (now + timedelta(hours=5)).isoformat(),
            "status" : "SCHEDULED"
            }
    response_flight = client.post(f"{api_url}/flights", json = flight_1)
    print(response_flight.json())
    assert response_flight.status_code == 201
    flight = response_flight.json()

    flight_update  = {
            "flight_number": f"TEST{str(uuid.uuid4())[:8].upper()}",
            "airline" : "TEST_UPDATE",
            "departure_airport_id" : depart_airport["id"],
            "arrival_airport_id" : ariv_airport["id"],
            "scheduled_departure": (now + timedelta(hours=2)).isoformat(),
            "scheduled_arrival": (now + timedelta(hours=5)).isoformat(),
            "status" : "TEST_UPDATE_SCHEDULED"
            }
    flight_id = flight["id"]
    response_update = client.put(f"{api_url}/flights/{flight_id}", json = flight_update)
    assert response_update.status_code == 200
    data_update = response_update.json()

    assert data_update["status"] == "TEST_UPDATE_SCHEDULED"
    assert data_update["airline"] == "TEST_UPDATE"

# Test negatifs :

def test_get_flight_not_found(client, api_url):
    fake_id = "00000000-0000-0000-0000-000000000000"
    response = client.get(f"{api_url}/flights/{fake_id}")
    assert response.status_code == 404


def test_update_flight_not_found(client, api_url):
    fake_id = "00000000-0000-0000-0000-000000000000"
    flight_update = {"origin": "XXX", "destination": "YYY"}
    response = client.put(f"{api_url}/flights/{fake_id}", json=flight_update)
    assert response.status_code == 404
    assert response.json()["detail"] == "Flight not found"


def test_delete_flight_not_found(client, api_url):
    fake_id = "00000000-0000-0000-0000-000000000000"
    response = client.delete(f"{api_url}/flights/{fake_id}")
    assert response.status_code == 404
    assert response.json()["detail"] == "Flight not found"

#def test_list_flights_empty(client, api_url):
    response = client.get(f"{api_url}/flights")
    assert response.status_code == 400
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

def test_delete_flight_not_found(client, api_url):
    fake_id = "00000000-0000-0000-0000-000000000000"
    response = client.delete(f"{api_url}/airports/{fake_id}")
    assert response.status_code == 404

