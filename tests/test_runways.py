import random
from uuid import uuid4
import uuid
from datetime import datetime, timedelta

def test_create_runways(client, api_url):

    airport_1 = {
            "code" : f"TEST{str(uuid.uuid4())[:8].upper()}",
            "name" : "Departue Airport",
            "city" : "Testcity",
            "country" : "Testcountry",
            "timezone" : "Testzone"
            }
    response_dep = client.post(f"{api_url}/airports", json = airport_1)
    assert response_dep.status_code == 201
    depart_airport = response_dep.json()

    runway_1 = {
            "runway_code" : "Testrunway_1",
            "length_meters" : 123,
            "width_meters" : 321,
            "surface_type" : "asphalt",
            "status" : "Open",
            "airport_id" : depart_airport["id"]
            }

    runway_2 = {
            "runway_code" : "Testrunway_2",
            "length_meters" : 321,
            "width_meters" : 123,
            "surface_type" : "asphalt",
            "status" : "Open",
            "airport_id" : depart_airport["id"]
            }

    dep_runway_resp = client.post(f"{api_url}/runways", json = runway_1)
    dep_runway = dep_runway_resp.json()
    assert dep_runway_resp.status_code == 201
    assert dep_runway["runway_code"] == "Testrunway_1"
    assert dep_runway["airport_id"] == depart_airport["id"]

    ariv_runway_resp = client.post(f"{api_url}/runways", json = runway_2)
    ariv_runway = ariv_runway_resp.json()
    assert ariv_runway_resp.status_code == 201
    assert ariv_runway["runway_code"] == "Testrunway_2"
    assert ariv_runway["airport_id"] == depart_airport["id"]

def test_delete_runway(client, api_url):

    airport_1 = {
            "code" : f"TEST{str(uuid.uuid4())[:8].upper()}",
            "name" : "Departue Airport",
            "city" : "Testcity",
            "country" : "Testcountry",
            "timezone" : "Testzone"
            }
    response_dep = client.post(f"{api_url}/airports", json = airport_1)
    assert response_dep.status_code == 201
    depart_airport = response_dep.json()

    runway_1 = {
            "runway_code" : "Testrunway_1",
            "length_meters" : 123,
            "width_meters" : 321,
            "surface_type" : "asphalt",
            "status" : "Open",
            "airport_id" : depart_airport["id"]
            }

    runway_2 = {
            "runway_code" : "Testrunway_2",
            "length_meters" : 321,
            "width_meters" : 123,
            "surface_type" : "asphalt",
            "status" : "Open",
            "airport_id" : depart_airport["id"]
            }

    dep_runway_resp = client.post(f"{api_url}/runways", json = runway_1)
    dep_runway = dep_runway_resp.json()
    assert dep_runway_resp.status_code == 201
    assert dep_runway["runway_code"] == "Testrunway_1"
    assert dep_runway["airport_id"] == depart_airport["id"]

    ariv_runway_resp = client.post(f"{api_url}/runways", json = runway_2)
    ariv_runway = ariv_runway_resp.json()
    assert ariv_runway_resp.status_code == 201
    assert ariv_runway["runway_code"] == "Testrunway_2"
    assert ariv_runway["airport_id"] == depart_airport["id"]
    
    id_runway = dep_runway["id"]
    response = client.delete(f"{api_url}/runways/{id_runway}")
    assert response.status_code == 200

def test_list_runway(client, api_url):
    response = client.get(f"{api_url}/runways")
    assert response.status_code == 200
    runways = response.json()
    assert isinstance(runways, list)

def test_update_runways(client, api_url):

    airport_1 = {
            "code" : f"TEST{str(uuid.uuid4())[:8].upper()}",
            "name" : "Departue Airport",
            "city" : "Testcity",
            "country" : "Testcountry",
            "timezone" : "Testzone"
            }
    response_dep = client.post(f"{api_url}/airports", json = airport_1)
    assert response_dep.status_code == 201
    depart_airport = response_dep.json()

    runway_1 = {
            "runway_code" : "Testrunway_1",
            "length_meters" : 123,
            "width_meters" : 321,
            "surface_type" : "asphalt",
            "status" : "Open",
            "airport_id" : depart_airport["id"]
            }

    runway_2 = {
            "runway_code" : "Testrunway_2",
            "length_meters" : 321,
            "width_meters" : 123,
            "surface_type" : "asphalt",
            "status" : "Open",
            "airport_id" : depart_airport["id"]
            }

    dep_runway_resp = client.post(f"{api_url}/runways", json = runway_1)
    dep_runway = dep_runway_resp.json()
    assert dep_runway_resp.status_code == 201
    assert dep_runway["runway_code"] == "Testrunway_1"
    assert dep_runway["airport_id"] == depart_airport["id"]

    ariv_runway_resp = client.post(f"{api_url}/runways", json = runway_2)
    ariv_runway = ariv_runway_resp.json()
    assert ariv_runway_resp.status_code == 201
    assert ariv_runway["runway_code"] == "Testrunway_2"
    assert ariv_runway["airport_id"] == depart_airport["id"]
    
    runway_update = {
            "runway_code" : "Testrunway_update",
            "length_meters" : 123,
            "width_meters" : 321,
            "surface_type" : "asphalt",
            "status" : "Test_update",
            "airport_id" : depart_airport["id"]
            }
    runway_id = dep_runway["id"] 
    response = client.put(f"{api_url}/runways/{runway_id}", json = runway_update)
    assert response.status_code == 200
    data_runway_update = response.json()
    assert data_runway_update["runway_code"] == "Testrunway_update"
    assert data_runway_update["status"] == "Test_update"

# Test negatifs :

def test_get_airport_not_found(client, api_url):
    fake_id = "00000000-0000-0000-0000-000000000000"
    response = client.get(f"{api_url}/runways/{fake_id}")
    assert response.status_code == 404


def test_update_runway_not_found(client, api_url):
    fake_id = "00000000-0000-0000-0000-000000000000"
    runway_update = {"origin": "XXX", "destination": "YYY"}
    response = client.put(f"{api_url}/runways/{fake_id}", json=runway_update)
    assert response.status_code == 404
    assert response.json()["detail"] == "Runway not found"


def test_delete_runway_not_found(client, api_url):
    fake_id = "00000000-0000-0000-0000-000000000000"
    response = client.delete(f"{api_url}/runways/{fake_id}")
    assert response.status_code == 404
    assert response.json()["detail"] == "Runway not found"

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

    response = client.post(f"{api_url}/runways", json=flight_data)

    print(response.status_code, response.text)

    assert response.status_code == 201
    runway_id = response.json()["id"]

    new_runway_id = str(uuid4())

    response = client.put(
        f"{api_url}/flights/{runway_id}",
        json={"departure_runway_id": new_runway_id}
    )

    assert response.status_code == 200

def test_delete_runway_not_found(client, api_url):
    fake_id = "00000000-0000-0000-0000-000000000000"
    response = client.delete(f"{api_url}/runways/{fake_id}")
    assert response.status_code == 404
