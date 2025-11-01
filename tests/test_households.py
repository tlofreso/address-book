from fastapi.testclient import TestClient


def test_create_household(client: TestClient):
    response = client.post(
        "/households/",
        json={
            "name": "The Lofreso's",
            "address": "438 Red Rock Dr",
        },
    )
    assert response.status_code == 200
    data = response.json()
    assert data["name"] == "The Lofreso's"
    assert data["address"] == "438 Red Rock Dr"
    assert "id" in data


def test_create_household_minimal(client: TestClient):
    response = client.post(
        "/households/",
        json={"name": "The Smith Family"},
    )
    assert response.status_code == 200
    data = response.json()
    assert data["name"] == "The Smith Family"
    assert data["address"] is None


def test_list_households(client: TestClient):
    client.post(
        "/households/",
        json={"name": "Household One", "address": "123 First St"},
    )
    client.post(
        "/households/",
        json={"name": "Household Two", "address": "456 Second Ave"},
    )

    response = client.get("/households/")
    assert response.status_code == 200
    data = response.json()
    assert len(data) == 2
    assert data[0]["name"] == "Household One"
    assert data[1]["name"] == "Household Two"


def test_get_household(client: TestClient):
    create_response = client.post(
        "/households/",
        json={"name": "Test Household", "address": "789 Test Lane"},
    )
    household_id = create_response.json()["id"]

    response = client.get(f"/households/{household_id}")
    assert response.status_code == 200
    data = response.json()
    assert data["id"] == household_id
    assert data["name"] == "Test Household"
    assert data["address"] == "789 Test Lane"


def test_get_household_not_found(client: TestClient):
    response = client.get("/households/999")
    assert response.status_code == 404
    assert response.json() == {"detail": "Household not found"}


def test_update_household(client: TestClient):
    create_response = client.post(
        "/households/",
        json={"name": "Original Name", "address": "Original Address"},
    )
    household_id = create_response.json()["id"]

    response = client.patch(
        f"/households/{household_id}",
        json={"name": "Updated Name"},
    )
    assert response.status_code == 200
    data = response.json()
    assert data["id"] == household_id
    assert data["name"] == "Updated Name"
    assert data["address"] == "Original Address"


def test_update_household_not_found(client: TestClient):
    response = client.patch(
        "/households/999",
        json={"name": "Test"},
    )
    assert response.status_code == 404
    assert response.json() == {"detail": "Household not found"}


def test_delete_household(client: TestClient):
    create_response = client.post(
        "/households/",
        json={"name": "To Delete", "address": "Delete St"},
    )
    household_id = create_response.json()["id"]

    response = client.delete(f"/households/{household_id}")
    assert response.status_code == 200
    assert response.json() == {"message": "Household deleted successfully"}

    get_response = client.get(f"/households/{household_id}")
    assert get_response.status_code == 404


def test_delete_household_not_found(client: TestClient):
    response = client.delete("/households/999")
    assert response.status_code == 404
    assert response.json() == {"detail": "Household not found"}


def test_get_household_members(client: TestClient):
    # Create household
    household_response = client.post(
        "/households/",
        json={"name": "Test Family", "address": "123 Family Lane"},
    )
    household_id = household_response.json()["id"]

    # Create contacts and add to household
    contact1 = client.post(
        "/contacts/",
        json={"first_name": "John", "last_name": "Doe", "household_id": household_id},
    )
    contact2 = client.post(
        "/contacts/",
        json={"first_name": "Jane", "last_name": "Doe", "household_id": household_id},
    )

    # Get household members
    response = client.get(f"/households/{household_id}/members")
    assert response.status_code == 200
    data = response.json()
    assert len(data) == 2
    assert data[0]["first_name"] == "John"
    assert data[1]["first_name"] == "Jane"


def test_get_household_members_not_found(client: TestClient):
    response = client.get("/households/999/members")
    assert response.status_code == 404
    assert response.json() == {"detail": "Household not found"}


def test_add_member_to_household(client: TestClient):
    # Create household
    household_response = client.post(
        "/households/",
        json={"name": "Test Household"},
    )
    household_id = household_response.json()["id"]

    # Create contact
    contact_response = client.post(
        "/contacts/",
        json={"first_name": "Bob", "last_name": "Smith"},
    )
    contact_id = contact_response.json()["id"]

    # Add contact to household
    response = client.post(f"/households/{household_id}/members/{contact_id}")
    assert response.status_code == 200
    assert response.json()["message"] == "Member added successfully"

    # Verify contact is now part of household
    contact = client.get(f"/contacts/{contact_id}").json()
    assert contact["household_id"] == household_id


def test_add_member_household_not_found(client: TestClient):
    contact_response = client.post(
        "/contacts/",
        json={"first_name": "Test", "last_name": "User"},
    )
    contact_id = contact_response.json()["id"]

    response = client.post(f"/households/999/members/{contact_id}")
    assert response.status_code == 404
    assert response.json() == {"detail": "Household not found"}


def test_add_member_contact_not_found(client: TestClient):
    household_response = client.post(
        "/households/",
        json={"name": "Test Household"},
    )
    household_id = household_response.json()["id"]

    response = client.post(f"/households/{household_id}/members/999")
    assert response.status_code == 404
    assert response.json() == {"detail": "Contact not found"}


def test_remove_member_from_household(client: TestClient):
    # Create household
    household_response = client.post(
        "/households/",
        json={"name": "Test Household"},
    )
    household_id = household_response.json()["id"]

    # Create contact with household
    contact_response = client.post(
        "/contacts/",
        json={"first_name": "Alice", "last_name": "Johnson", "household_id": household_id},
    )
    contact_id = contact_response.json()["id"]

    # Remove from household
    response = client.delete(f"/households/{household_id}/members/{contact_id}")
    assert response.status_code == 200
    assert response.json()["message"] == "Member removed successfully"

    # Verify contact no longer has household
    contact = client.get(f"/contacts/{contact_id}").json()
    assert contact["household_id"] is None


def test_remove_member_household_not_found(client: TestClient):
    contact_response = client.post(
        "/contacts/",
        json={"first_name": "Test", "last_name": "User"},
    )
    contact_id = contact_response.json()["id"]

    response = client.delete(f"/households/999/members/{contact_id}")
    assert response.status_code == 404
    assert response.json() == {"detail": "Household not found"}


def test_remove_member_contact_not_found(client: TestClient):
    household_response = client.post(
        "/households/",
        json={"name": "Test Household"},
    )
    household_id = household_response.json()["id"]

    response = client.delete(f"/households/{household_id}/members/999")
    assert response.status_code == 404
    assert response.json() == {"detail": "Contact not found"}


def test_remove_member_not_in_household(client: TestClient):
    # Create two households
    household1_response = client.post(
        "/households/",
        json={"name": "Household 1"},
    )
    household1_id = household1_response.json()["id"]

    household2_response = client.post(
        "/households/",
        json={"name": "Household 2"},
    )
    household2_id = household2_response.json()["id"]

    # Create contact in household1
    contact_response = client.post(
        "/contacts/",
        json={"first_name": "Test", "last_name": "User", "household_id": household1_id},
    )
    contact_id = contact_response.json()["id"]

    # Try to remove from household2
    response = client.delete(f"/households/{household2_id}/members/{contact_id}")
    assert response.status_code == 400
    assert response.json() == {"detail": "Contact is not a member of this household"}


def test_contact_with_household(client: TestClient):
    # Create household first
    household_response = client.post(
        "/households/",
        json={"name": "The Browns", "address": "100 Oak Street"},
    )
    household_id = household_response.json()["id"]

    # Create contact with household
    response = client.post(
        "/contacts/",
        json={
            "first_name": "Charlie",
            "last_name": "Brown",
            "household_id": household_id,
        },
    )
    assert response.status_code == 200
    data = response.json()
    assert data["first_name"] == "Charlie"
    assert data["household_id"] == household_id


def test_update_contact_household(client: TestClient):
    # Create household
    household_response = client.post(
        "/households/",
        json={"name": "New Household"},
    )
    household_id = household_response.json()["id"]

    # Create contact without household
    contact_response = client.post(
        "/contacts/",
        json={"first_name": "Test", "last_name": "User"},
    )
    contact_id = contact_response.json()["id"]

    # Update contact to add household
    response = client.patch(
        f"/contacts/{contact_id}",
        json={"household_id": household_id},
    )
    assert response.status_code == 200
    data = response.json()
    assert data["household_id"] == household_id
