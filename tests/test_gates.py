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

    gate_1 = {
            "gate_code" : "Gate_test1",
            "terminal" : "Terminal_test_1",
            "status" : "Test_status",
            "gate_type" : "Test_gate_type",
            "airport_id" : depart_airport["id"]
            }
    gate_2 = {
            "gate_code" : "Gate_test2",
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

    ariv_gate_resp = client.post(f"{api_url}/gates", json = gate_2)
    assert ariv_gate_resp.status_code == 201
    ariv_gate = ariv_gate_resp.json()
    assert ariv_gate["airport_id"] == depart_airport["id"]
    assert ariv_gate["gate_code"] == "Gate_test2"
    
def test_list_gates(client, api_url):
    response = client.get(f"{api_url}/gates")
    assert response.status_code == 200
    gates = response.json()
    assert isinstance(gates, list)
