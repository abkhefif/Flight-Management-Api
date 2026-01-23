from datetime import datetime, timedelta
from uuid import uuid4

def test_list_slots(client, api_url):
    response = client.get(f"{api_url}/slots")
    assert response.status_code == 200
    assert isinstance(response.json(), list)

def test_create_slot(client, api_url):
    airport_id = client.post(
        f"{api_url}/airports",
        json={
            "code": f"TEST{str(uuid4())[:8]}",
            "name": "Slot Airport",
            "city": "City",
            "country": "Country",
            "timezone": "UTC"
        }
    ).json()["id"]

    runway_id = client.post(
        f"{api_url}/runways",
        json={
            "runway_code": "RWY_TEST",
            "length_meters": 3000,
            "width_meters": 45,
            "surface_type": "asphalt",
            "status": "AVAILABLE",
            "airport_id": airport_id
        }
    ).json()["id"]

    now = datetime.utcnow()

    slot_data = {
        "slot_type": "DEPARTURE",
        "airport_id": airport_id,
        "runway_id": runway_id,
        "status": "AVAILABLE",
        "start_time": now.isoformat(),
        "end_time": (now + timedelta(minutes=30)).isoformat()
    }

    response = client.post(f"{api_url}/slots", json=slot_data)

    assert response.status_code == 201
    data = response.json()
    assert "id" in data

def test_get_slot_by_id(client, api_url):
    airport_id = client.post(
        f"{api_url}/airports",
        json={
            "code": f"TEST{str(uuid4())[:8]}",
            "name": "Slot Airport",
            "city": "City",
            "country": "Country",
            "timezone": "UTC"
        }
    ).json()["id"]

    runway_id = client.post(
        f"{api_url}/runways",
        json={
            "runway_code": "RWY_TEST",
            "length_meters": 3000,
            "width_meters": 45,
            "surface_type": "asphalt",
            "status": "AVAILABLE",
            "airport_id": airport_id
        }
    ).json()["id"]

    now = datetime.utcnow()

    slot_resp = client.post(
        f"{api_url}/slots",
        json={
            "slot_type": "ARRIVAL",
            "status": "AVAILABLE",
            "airport_id": airport_id,
            "runway_id": runway_id,
            "start_time": now.isoformat(),
            "end_time": (now + timedelta(minutes=30)).isoformat()
        }
    )

    assert slot_resp.status_code == 201
    slot_id = slot_resp.json()["id"]

    get_resp = client.get(f"{api_url}/slots/{slot_id}")
    assert get_resp.status_code == 200

def test_update_slot(client, api_url):
    airport_id = client.post(
        f"{api_url}/airports",
        json={
            "code": f"TEST{str(uuid4())[:8]}",
            "name": "Slot Airport",
            "city": "City",
            "country": "Country",
            "timezone": "UTC"
        }
    ).json()["id"]

    runway_id = client.post(
        f"{api_url}/runways",
        json={
            "runway_code": "RWY_TEST",
            "length_meters": 3000,
            "width_meters": 45,
            "surface_type": "asphalt",
            "status": "AVAILABLE",
            "airport_id": airport_id
        }
    ).json()["id"]

    now = datetime.utcnow()

    slot_resp = client.post(
        f"{api_url}/slots",
        json={
            "slot_type": "DEPARTURE",
            "status": "AVAILABLE",
            "airport_id": airport_id,
            "runway_id": runway_id,
            "start_time": now.isoformat(),
            "end_time": (now + timedelta(minutes=30)).isoformat()
        }
    )

    assert slot_resp.status_code == 201
    slot_id = slot_resp.json()["id"]

    response = client.put(
        f"{api_url}/slots/{slot_id}",
        json={"status": "RESERVED"}
    )

    assert response.status_code == 200
    assert response.json()["status"] == "RESERVED"

def test_delete_slot(client, api_url):
    airport_id = client.post(
        f"{api_url}/airports",
        json={
            "code": f"TEST{str(uuid4())[:8]}",
            "name": "Slot Airport",
            "city": "City",
            "country": "Country",
            "timezone": "UTC"
        }
    ).json()["id"]

    runway_id = client.post(
        f"{api_url}/runways",
        json={
            "runway_code": "RWY_TEST",
            "length_meters": 3000,
            "width_meters": 45,
            "surface_type": "asphalt",
            "status": "AVAILABLE",
            "airport_id": airport_id
        }
    ).json()["id"]

    now = datetime.utcnow()

    slot_resp = client.post(
        f"{api_url}/slots",
        json={
            "slot_type": "DEPARTURE",
            "status": "AVAILABLE",
            "airport_id": airport_id,
            "runway_id": runway_id,
            "start_time": now.isoformat(),
            "end_time": (now + timedelta(minutes=30)).isoformat()
        }
    )

    assert slot_resp.status_code == 201
    slot_id = slot_resp.json()["id"]

    delete_resp = client.delete(f"{api_url}/slots/{slot_id}")
    assert delete_resp.status_code == 200

    get_resp = client.get(f"{api_url}/slots/{slot_id}")
    assert get_resp.status_code == 404

#test issues:

def test_get_slot_not_found(client, api_url):
    fake_id = "00000000-0000-0000-0000-000000000000"
    response = client.get(f"{api_url}/slots/{fake_id}")
    assert response.status_code == 404
    assert response.json()["detail"] == "Slot not found"

def test_update_slot_not_found(client, api_url):
    fake_id = "00000000-0000-0000-0000-000000000000"
    response = client.put(f"{api_url}/slots/{fake_id}", json={"end_time": datetime.utcnow().isoformat()})
    assert response.status_code == 404
    assert response.json()["detail"] == "Slot not found"

def test_create_slot_too_short(client, api_url):
    now = datetime.utcnow()

    slot = {
        "slot_type": "DEPARTURE",
        "airport_id": "...",
        "runway_id": "...",
        "status": "AVAILABLE",
        "start_time": now.isoformat(),
        "end_time": (now + timedelta(minutes=5)).isoformat()
    }

    resp = client.post(f"{api_url}/slots", json=slot)
    assert resp.status_code == 422

