from fastapi.testclient import TestClient


def test_root(client: TestClient):
    response = client.get("/")
    assert response.status_code == 200
    assert "text/html" in response.headers["content-type"]


def test_create_household_with_members(client: TestClient):
    response = client.post(
        "/households/",
        json={
            "name": "The Lofreso's",
            "address": "438 Red Rock Dr",
            "members": [
                {"first_name": "Tony", "last_name": "Lofreso", "email": None, "phone": None},
                {"first_name": "Bridgette", "last_name": "Lofreso", "email": None, "phone": None},
                {"first_name": "Theodore", "last_name": "Lofreso", "email": None, "phone": None},
                {"first_name": "Ruthie", "last_name": "Lofreso", "email": None, "phone": None},
            ],
        },
    )
    data = response.json()

    assert response.status_code == 200
    assert data["name"] == "The Lofreso's"
    assert data["address"] == "438 Red Rock Dr"
    assert len(data["members"]) == 4
    assert data["members"][0]["first_name"] == "Tony"
    assert data["members"][0]["last_name"] == "Lofreso"


def test_create_household_minimal(client: TestClient):
    response = client.post(
        "/households/",
        json={
            "name": "The Smith's",
            "address": "123 Main St",
            "members": [],
        },
    )
    data = response.json()

    assert response.status_code == 200
    assert data["name"] == "The Smith's"
    assert data["address"] == "123 Main St"
    assert len(data["members"]) == 0


def test_list_households(client: TestClient):
    # Create a household first
    client.post(
        "/households/",
        json={
            "name": "Test Household",
            "address": "123 Test St",
            "members": [{"first_name": "John", "last_name": "Doe", "email": None, "phone": None}],
        },
    )

    response = client.get("/households/")
    data = response.json()

    assert response.status_code == 200
    assert isinstance(data, list)
    assert len(data) >= 1
    assert data[-1]["name"] == "Test Household"


def test_get_household(client: TestClient):
    # Create a household
    create_response = client.post(
        "/households/",
        json={
            "name": "Get Test Household",
            "address": "456 Get St",
            "members": [{"first_name": "Jane", "last_name": "Doe", "email": None, "phone": None}],
        },
    )
    household_id = create_response.json()["id"]

    # Get the household
    response = client.get(f"/households/{household_id}")
    data = response.json()

    assert response.status_code == 200
    assert data["id"] == household_id
    assert data["name"] == "Get Test Household"
    assert data["address"] == "456 Get St"
    assert len(data["members"]) == 1


def test_get_household_not_found(client: TestClient):
    response = client.get("/households/99999")
    assert response.status_code == 404


def test_update_household(client: TestClient):
    # Create a household
    create_response = client.post(
        "/households/",
        json={
            "name": "Original Name",
            "address": "Original Address",
            "members": [],
        },
    )
    household_id = create_response.json()["id"]

    # Update the household
    response = client.patch(
        f"/households/{household_id}",
        json={
            "name": "Updated Name",
            "address": "Updated Address",
        },
    )
    data = response.json()

    assert response.status_code == 200
    assert data["name"] == "Updated Name"
    assert data["address"] == "Updated Address"


def test_update_household_not_found(client: TestClient):
    response = client.patch(
        "/households/99999",
        json={"name": "Should Fail"},
    )
    assert response.status_code == 404


def test_delete_household(client: TestClient):
    # Create a household
    create_response = client.post(
        "/households/",
        json={
            "name": "To Delete",
            "address": "Delete St",
            "members": [{"first_name": "Will", "last_name": "Delete", "email": None, "phone": None}],
        },
    )
    household_id = create_response.json()["id"]

    # Delete the household
    response = client.delete(f"/households/{household_id}")
    assert response.status_code == 200

    # Verify it's deleted
    get_response = client.get(f"/households/{household_id}")
    assert get_response.status_code == 404


def test_delete_household_not_found(client: TestClient):
    response = client.delete("/households/99999")
    assert response.status_code == 404


def test_add_member_to_household(client: TestClient):
    # Create a household
    create_response = client.post(
        "/households/",
        json={
            "name": "Add Member Test",
            "address": "123 Member St",
            "members": [],
        },
    )
    household_id = create_response.json()["id"]

    # Add a member
    response = client.post(
        f"/households/{household_id}/members",
        json={
            "first_name": "New",
            "last_name": "Member",
            "email": "new@example.com",
            "phone": "555-1234",
        },
    )
    data = response.json()

    assert response.status_code == 200
    assert data["first_name"] == "New"
    assert data["last_name"] == "Member"
    assert data["email"] == "new@example.com"
    assert data["phone"] == "555-1234"
    assert data["household_id"] == household_id


def test_add_member_to_nonexistent_household(client: TestClient):
    response = client.post(
        "/households/99999/members",
        json={
            "first_name": "Should",
            "last_name": "Fail",
            "email": None,
            "phone": None,
        },
    )
    assert response.status_code == 404


def test_update_member(client: TestClient):
    # Create a household with a member
    create_response = client.post(
        "/households/",
        json={
            "name": "Update Member Test",
            "address": "123 Update St",
            "members": [{"first_name": "Original", "last_name": "Name", "email": None, "phone": None}],
        },
    )
    data = create_response.json()
    household_id = data["id"]
    member_id = data["members"][0]["id"]

    # Update the member
    response = client.patch(
        f"/households/{household_id}/members/{member_id}",
        json={
            "first_name": "Updated",
            "last_name": "Member",
        },
    )
    updated_data = response.json()

    assert response.status_code == 200
    assert updated_data["first_name"] == "Updated"
    assert updated_data["last_name"] == "Member"


def test_update_member_not_found(client: TestClient):
    response = client.patch(
        "/households/1/members/99999",
        json={"first_name": "Should Fail"},
    )
    assert response.status_code == 404


def test_update_member_wrong_household(client: TestClient):
    # Create two households
    household1 = client.post(
        "/households/",
        json={
            "name": "Household 1",
            "address": "123 First St",
            "members": [{"first_name": "Member", "last_name": "One", "email": None, "phone": None}],
        },
    ).json()

    household2 = client.post(
        "/households/",
        json={
            "name": "Household 2",
            "address": "456 Second St",
            "members": [],
        },
    ).json()

    # Try to update member from household 1 using household 2's ID
    member_id = household1["members"][0]["id"]
    household2_id = household2["id"]

    response = client.patch(
        f"/households/{household2_id}/members/{member_id}",
        json={"first_name": "Should Fail"},
    )
    assert response.status_code == 404


def test_remove_member(client: TestClient):
    # Create a household with a member
    create_response = client.post(
        "/households/",
        json={
            "name": "Remove Member Test",
            "address": "123 Remove St",
            "members": [{"first_name": "To", "last_name": "Remove", "email": None, "phone": None}],
        },
    )
    data = create_response.json()
    household_id = data["id"]
    member_id = data["members"][0]["id"]

    # Remove the member
    response = client.delete(f"/households/{household_id}/members/{member_id}")
    assert response.status_code == 200

    # Verify household still exists but has no members
    household = client.get(f"/households/{household_id}").json()
    assert len(household["members"]) == 0


def test_remove_member_not_found(client: TestClient):
    response = client.delete("/households/1/members/99999")
    assert response.status_code == 404


def test_cascade_delete_members(client: TestClient):
    # Create a household with multiple members
    create_response = client.post(
        "/households/",
        json={
            "name": "Cascade Test",
            "address": "123 Cascade St",
            "members": [
                {"first_name": "Member", "last_name": "One", "email": None, "phone": None},
                {"first_name": "Member", "last_name": "Two", "email": None, "phone": None},
            ],
        },
    )
    household_id = create_response.json()["id"]

    # Delete the household
    delete_response = client.delete(f"/households/{household_id}")
    assert delete_response.status_code == 200

    # Verify household is deleted
    get_response = client.get(f"/households/{household_id}")
    assert get_response.status_code == 404
