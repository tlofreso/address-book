from fastapi.testclient import TestClient


def test_create_list(client: TestClient):
    response = client.post(
        "/lists/",
        json={"name": "Christmas Cards", "description": "Annual holiday card list"},
    )
    data = response.json()

    assert response.status_code == 200
    assert data["name"] == "Christmas Cards"
    assert data["description"] == "Annual holiday card list"
    assert data["household_count"] == 0


def test_create_list_minimal(client: TestClient):
    response = client.post(
        "/lists/",
        json={"name": "Birthday Party"},
    )
    data = response.json()

    assert response.status_code == 200
    assert data["name"] == "Birthday Party"
    assert data["household_count"] == 0


def test_list_lists(client: TestClient):
    # Create a couple of lists
    client.post("/lists/", json={"name": "List 1"})
    client.post("/lists/", json={"name": "List 2", "description": "Test list"})

    response = client.get("/lists/")
    data = response.json()

    assert response.status_code == 200
    assert isinstance(data, list)
    assert len(data) >= 2


def test_get_list(client: TestClient):
    # Create a list
    create_response = client.post(
        "/lists/", json={"name": "Get Test List", "description": "Testing get"}
    )
    list_id = create_response.json()["id"]

    # Get the list
    response = client.get(f"/lists/{list_id}")
    data = response.json()

    assert response.status_code == 200
    assert data["id"] == list_id
    assert data["name"] == "Get Test List"
    assert data["description"] == "Testing get"
    assert "households" in data


def test_get_list_not_found(client: TestClient):
    response = client.get("/lists/99999")
    assert response.status_code == 404


def test_update_list(client: TestClient):
    # Create a list
    create_response = client.post(
        "/lists/", json={"name": "Original Name", "description": "Original"}
    )
    list_id = create_response.json()["id"]

    # Update the list
    response = client.patch(
        f"/lists/{list_id}",
        json={"name": "Updated Name", "description": "Updated description"},
    )
    data = response.json()

    assert response.status_code == 200
    assert data["name"] == "Updated Name"
    assert data["description"] == "Updated description"


def test_update_list_not_found(client: TestClient):
    response = client.patch("/lists/99999", json={"name": "Should Fail"})
    assert response.status_code == 404


def test_delete_list(client: TestClient):
    # Create a list
    create_response = client.post("/lists/", json={"name": "To Delete"})
    list_id = create_response.json()["id"]

    # Delete the list
    response = client.delete(f"/lists/{list_id}")
    assert response.status_code == 200

    # Verify it's deleted
    get_response = client.get(f"/lists/{list_id}")
    assert get_response.status_code == 404


def test_delete_list_not_found(client: TestClient):
    response = client.delete("/lists/99999")
    assert response.status_code == 404


def test_add_household_to_list(client: TestClient):
    # Create a household
    household_response = client.post(
        "/households/",
        json={
            "name": "Test Household",
            "address": "123 Test St",
            "members": [],
        },
    )
    household_id = household_response.json()["id"]

    # Create a list
    list_response = client.post("/lists/", json={"name": "Test List"})
    list_id = list_response.json()["id"]

    # Add household to list
    response = client.post(f"/lists/{list_id}/households/{household_id}")
    assert response.status_code == 200

    # Verify household is in list
    list_data = client.get(f"/lists/{list_id}").json()
    assert len(list_data["households"]) == 1
    assert list_data["households"][0]["id"] == household_id


def test_add_household_to_list_duplicate(client: TestClient):
    # Create a household and list
    household_id = client.post(
        "/households/",
        json={"name": "Test", "address": "Test", "members": []},
    ).json()["id"]
    list_id = client.post("/lists/", json={"name": "Test"}).json()["id"]

    # Add household to list
    client.post(f"/lists/{list_id}/households/{household_id}")

    # Try to add again
    response = client.post(f"/lists/{list_id}/households/{household_id}")
    assert response.status_code == 200
    assert "already in list" in response.json()["message"].lower()


def test_add_household_to_nonexistent_list(client: TestClient):
    response = client.post("/lists/99999/households/1")
    assert response.status_code == 404


def test_add_nonexistent_household_to_list(client: TestClient):
    list_id = client.post("/lists/", json={"name": "Test"}).json()["id"]
    response = client.post(f"/lists/{list_id}/households/99999")
    assert response.status_code == 404


def test_add_multiple_households_to_list(client: TestClient):
    # Create households
    household1_id = client.post(
        "/households/",
        json={"name": "Household 1", "address": "123 St", "members": []},
    ).json()["id"]
    household2_id = client.post(
        "/households/",
        json={"name": "Household 2", "address": "456 Ave", "members": []},
    ).json()["id"]
    household3_id = client.post(
        "/households/",
        json={"name": "Household 3", "address": "789 Ln", "members": []},
    ).json()["id"]

    # Create a list
    list_id = client.post("/lists/", json={"name": "Bulk Test"}).json()["id"]

    # Add multiple households
    response = client.post(
        f"/lists/{list_id}/households/bulk",
        json={"household_ids": [household1_id, household2_id, household3_id]},
    )

    if response.status_code != 200:
        print(f"Error: {response.json()}")

    data = response.json()

    assert response.status_code == 200
    assert "3" in data["message"]

    # Verify all households are in list
    list_data = client.get(f"/lists/{list_id}").json()
    assert len(list_data["households"]) == 3


def test_bulk_add_with_invalid_ids(client: TestClient):
    # Create one valid household
    household_id = client.post(
        "/households/",
        json={"name": "Valid", "address": "123 St", "members": []},
    ).json()["id"]

    # Create a list
    list_id = client.post("/lists/", json={"name": "Test"}).json()["id"]

    # Try to add valid and invalid households
    response = client.post(
        f"/lists/{list_id}/households/bulk",
        json={"household_ids": [household_id, 99999, 88888]},
    )
    data = response.json()

    assert response.status_code == 200
    # Should only add the valid one
    assert "1" in data["message"]


def test_remove_household_from_list(client: TestClient):
    # Create household and list
    household_id = client.post(
        "/households/",
        json={"name": "Test", "address": "Test", "members": []},
    ).json()["id"]
    list_id = client.post("/lists/", json={"name": "Test"}).json()["id"]

    # Add household to list
    client.post(f"/lists/{list_id}/households/{household_id}")

    # Remove household from list
    response = client.delete(f"/lists/{list_id}/households/{household_id}")
    assert response.status_code == 200

    # Verify household is removed
    list_data = client.get(f"/lists/{list_id}").json()
    assert len(list_data["households"]) == 0


def test_remove_household_not_in_list(client: TestClient):
    # Create household and list
    household_id = client.post(
        "/households/",
        json={"name": "Test", "address": "Test", "members": []},
    ).json()["id"]
    list_id = client.post("/lists/", json={"name": "Test"}).json()["id"]

    # Try to remove household that's not in list
    response = client.delete(f"/lists/{list_id}/households/{household_id}")
    assert response.status_code == 404


def test_delete_list_preserves_households(client: TestClient):
    # Create household and list
    household_id = client.post(
        "/households/",
        json={"name": "Test", "address": "Test", "members": []},
    ).json()["id"]
    list_id = client.post("/lists/", json={"name": "Test"}).json()["id"]

    # Add household to list
    client.post(f"/lists/{list_id}/households/{household_id}")

    # Delete the list
    client.delete(f"/lists/{list_id}")

    # Verify household still exists
    household_response = client.get(f"/households/{household_id}")
    assert household_response.status_code == 200


def test_delete_household_removes_from_lists(client: TestClient):
    # Create household
    household_id = client.post(
        "/households/",
        json={"name": "Test", "address": "Test", "members": []},
    ).json()["id"]

    # Create multiple lists and add household to them
    list1_id = client.post("/lists/", json={"name": "List 1"}).json()["id"]
    list2_id = client.post("/lists/", json={"name": "List 2"}).json()["id"]

    client.post(f"/lists/{list1_id}/households/{household_id}")
    client.post(f"/lists/{list2_id}/households/{household_id}")

    # Delete the household
    client.delete(f"/households/{household_id}")

    # Verify household is removed from both lists
    list1_data = client.get(f"/lists/{list1_id}").json()
    list2_data = client.get(f"/lists/{list2_id}").json()

    assert len(list1_data["households"]) == 0
    assert len(list2_data["households"]) == 0
