from fastapi.testclient import TestClient


def test_read_root(client: TestClient):
    response = client.get("/")
    assert response.status_code == 200
    assert "text/html" in response.headers["content-type"]
    assert "Address Book" in response.text


def test_create_contact(client: TestClient):
    response = client.post(
        "/contacts/",
        json={
            "first_name": "John",
            "last_name": "Doe",
            "email": "john.doe@example.com",
            "phone": "555-1234",
            "address": "123 Main St",
        },
    )
    assert response.status_code == 200
    data = response.json()
    assert data["first_name"] == "John"
    assert data["last_name"] == "Doe"
    assert data["email"] == "john.doe@example.com"
    assert data["phone"] == "555-1234"
    assert data["address"] == "123 Main St"
    assert "id" in data


def test_create_contact_minimal(client: TestClient):
    response = client.post(
        "/contacts/",
        json={"first_name": "Jane", "last_name": "Smith"},
    )
    assert response.status_code == 200
    data = response.json()
    assert data["first_name"] == "Jane"
    assert data["last_name"] == "Smith"
    assert data["email"] is None
    assert data["phone"] is None
    assert data["address"] is None


def test_list_contacts(client: TestClient):
    client.post(
        "/contacts/",
        json={"first_name": "Alice", "last_name": "Johnson"},
    )
    client.post(
        "/contacts/",
        json={"first_name": "Bob", "last_name": "Williams"},
    )

    response = client.get("/contacts/")
    assert response.status_code == 200
    data = response.json()
    assert len(data) == 2
    assert data[0]["first_name"] == "Alice"
    assert data[1]["first_name"] == "Bob"


def test_get_contact(client: TestClient):
    create_response = client.post(
        "/contacts/",
        json={"first_name": "Charlie", "last_name": "Brown"},
    )
    contact_id = create_response.json()["id"]

    response = client.get(f"/contacts/{contact_id}")
    assert response.status_code == 200
    data = response.json()
    assert data["id"] == contact_id
    assert data["first_name"] == "Charlie"
    assert data["last_name"] == "Brown"


def test_get_contact_not_found(client: TestClient):
    response = client.get("/contacts/999")
    assert response.status_code == 404
    assert response.json() == {"detail": "Contact not found"}


def test_update_contact(client: TestClient):
    create_response = client.post(
        "/contacts/",
        json={"first_name": "David", "last_name": "Miller"},
    )
    contact_id = create_response.json()["id"]

    response = client.patch(
        f"/contacts/{contact_id}",
        json={"email": "david.miller@example.com", "phone": "555-5678"},
    )
    assert response.status_code == 200
    data = response.json()
    assert data["id"] == contact_id
    assert data["first_name"] == "David"
    assert data["last_name"] == "Miller"
    assert data["email"] == "david.miller@example.com"
    assert data["phone"] == "555-5678"


def test_update_contact_not_found(client: TestClient):
    response = client.patch(
        "/contacts/999",
        json={"email": "test@example.com"},
    )
    assert response.status_code == 404
    assert response.json() == {"detail": "Contact not found"}


def test_delete_contact(client: TestClient):
    create_response = client.post(
        "/contacts/",
        json={"first_name": "Eve", "last_name": "Davis"},
    )
    contact_id = create_response.json()["id"]

    response = client.delete(f"/contacts/{contact_id}")
    assert response.status_code == 200
    assert response.json() == {"message": "Contact deleted successfully"}

    get_response = client.get(f"/contacts/{contact_id}")
    assert get_response.status_code == 404


def test_delete_contact_not_found(client: TestClient):
    response = client.delete("/contacts/999")
    assert response.status_code == 404
    assert response.json() == {"detail": "Contact not found"}
