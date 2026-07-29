def register_test_user(client):
    response = client.post(
        "/users/register",
        json={
            "username": "calcuser",
            "email": "calc@example.com",
            "password": "Password123",
        },
    )

    assert response.status_code == 201
    return response.json()["id"]


def test_create_calculation(client):
    user_id = register_test_user(client)

    response = client.post(
        "/calculations",
        json={
            "a": 10,
            "b": 5,
            "type": "Add",
            "user_id": user_id,
        },
    )

    assert response.status_code == 201

    data = response.json()

    assert data["a"] == 10
    assert data["b"] == 5
    assert data["type"] == "Add"
    assert data["result"] == 15
    assert data["user_id"] == user_id


def test_browse_calculations(client):
    user_id = register_test_user(client)

    client.post(
        "/calculations",
        json={
            "a": 8,
            "b": 2,
            "type": "Divide",
            "user_id": user_id,
        },
    )

    response = client.get("/calculations")

    assert response.status_code == 200

    data = response.json()

    assert len(data) == 1
    assert data[0]["result"] == 4
    assert data[0]["type"] == "Divide"


def test_read_calculation(client):
    user_id = register_test_user(client)

    create_response = client.post(
        "/calculations",
        json={
            "a": 9,
            "b": 3,
            "type": "Multiply",
            "user_id": user_id,
        },
    )

    calculation_id = create_response.json()["id"]

    response = client.get(
        f"/calculations/{calculation_id}"
    )

    assert response.status_code == 200

    data = response.json()

    assert data["id"] == calculation_id
    assert data["result"] == 27


def test_update_calculation(client):
    user_id = register_test_user(client)

    create_response = client.post(
        "/calculations",
        json={
            "a": 10,
            "b": 5,
            "type": "Add",
            "user_id": user_id,
        },
    )

    calculation_id = create_response.json()["id"]

    response = client.put(
        f"/calculations/{calculation_id}",
        json={
            "a": 20,
            "b": 4,
            "type": "Multiply",
            "user_id": user_id,
        },
    )

    assert response.status_code == 200

    data = response.json()

    assert data["a"] == 20
    assert data["b"] == 4
    assert data["type"] == "Multiply"
    assert data["result"] == 80


def test_delete_calculation(client):
    user_id = register_test_user(client)

    create_response = client.post(
        "/calculations",
        json={
            "a": 15,
            "b": 5,
            "type": "Sub",
            "user_id": user_id,
        },
    )

    calculation_id = create_response.json()["id"]

    delete_response = client.delete(
        f"/calculations/{calculation_id}"
    )

    assert delete_response.status_code == 200
    assert delete_response.json() == {
        "message": "Calculation deleted successfully"
    }

    get_response = client.get(
        f"/calculations/{calculation_id}"
    )

    assert get_response.status_code == 404
    assert (
        get_response.json()["error"]
        == "Calculation not found"
    )


def test_read_nonexistent_calculation(client):
    response = client.get("/calculations/999")

    assert response.status_code == 404
    assert (
        response.json()["error"]
        == "Calculation not found"
    )


def test_update_nonexistent_calculation(client):
    response = client.put(
        "/calculations/999",
        json={
            "a": 2,
            "b": 3,
            "type": "Add",
            "user_id": None,
        },
    )

    assert response.status_code == 404
    assert (
        response.json()["error"]
        == "Calculation not found"
    )


def test_delete_nonexistent_calculation(client):
    response = client.delete("/calculations/999")

    assert response.status_code == 404
    assert (
        response.json()["error"]
        == "Calculation not found"
    )


def test_divide_by_zero_is_rejected(client):
    response = client.post(
        "/calculations",
        json={
            "a": 10,
            "b": 0,
            "type": "Divide",
            "user_id": None,
        },
    )

    assert response.status_code == 400
    assert "Cannot divide by zero" in response.json()["error"]


def test_invalid_calculation_type_is_rejected(client):
    response = client.post(
        "/calculations",
        json={
            "a": 10,
            "b": 5,
            "type": "Power",
            "user_id": None,
        },
    )

    assert response.status_code == 400
    assert "type" in response.json()["error"]