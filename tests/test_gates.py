import pytest
import uuid
import random
from uuid import uuid4
from datetime import datetime, timedelta

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


# Test negatifs :

def test_get_gate_not_found(client, api_url):
    fake_id = "00000000-0000-0000-0000-000000000000"
    response = client.get(f"{api_url}/gates/{fake_id}")
    assert response.status_code == 404
    assert response.json()["detail"] == "Gate not found"


def test_update_gate_not_found(client, api_url):
    fake_id = "00000000-0000-0000-0000-000000000000"
    flight_update = {"origin": "XXX", "destination": "YYY"}
    response = client.put(f"{api_url}/gates/{fake_id}", json=flight_update)
    assert response.status_code == 404
    assert response.json()["detail"] == "Gate not found"

def test_list_gates_empty(client, api_url):
    response = client.get(f"{api_url}/gates")
    assert response.status_code == 200
    assert response.json() == []

def test_update_gate_uuid_field(client, api_url):
    gate_data = {
        "gate_code": f"GATE-{str(uuid4())[:8]}",
        "terminal": "Test Terminal",
        "status": "AVAILABLE",
        "gate_type": "PAX",
        "airport_id": str(uuid4())  # Ici il faudrait idéalement un airport existant
    }

    response_create = client.post(f"{api_url}/gates", json=gate_data)
    assert response_create.status_code == 201
    gate = response_create.json()
    gate_id = gate["id"]

    # 2️⃣ Mise à jour avec un nouvel UUID (simule le déplacement sur un autre airport)
    new_airport_id = str(uuid4())
    gate_update = {
        "airport_id": new_airport_id,
        "status": "MAINTENANCE"
    }

    response_update = client.put(f"{api_url}/gates/{gate_id}", json=gate_update)
    assert response_update.status_code == 200
    updated_gate = response_update.json()

    # 3️⃣ Vérifications
    assert updated_gate["id"] == gate_id
    assert updated_gate["airport_id"] == new_airport_id
    assert updated_gate["status"] == "MAINTENANCE"

    # 4️⃣ Cas négatif : update d'un gate inexistant
    fake_id = "00000000-0000-0000-0000-000000000000"
    response_fake = client.put(f"{api_url}/gates/{fake_id}", json=gate_update)
    assert response_fake.status_code == 404
    assert response_fake.json()["detail"] == "Gate not found"

def test_delete_gates_not_found(client, api_url):
    fake_id = "00000000-0000-0000-0000-000000000000"
    response = client.delete(f"{api_url}/gates/{fake_id}")
    assert response.status_code == 404
