import random
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
