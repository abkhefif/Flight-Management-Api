import random
import uuid

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
#    for key in airport_data:
#        assert airport_data[key] ==  data[key]
    assert data["code"] == code
    assert data["name"] == "Test Airport"
    assert data["city"] == "Test City"
    assert data["country"] == "Test Country"
    assert data["timezone"] == "UTC"
