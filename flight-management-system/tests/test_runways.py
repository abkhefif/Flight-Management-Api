import pytest
import uuid
import random

def test_runways(client, api_url):

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


def test_list_runway(client, api_url):
    response = client.get(f"{api_url}/runways")
    assert response.status_code == 200
    runways = response.json()
    assert isinstance(runways, list)
