def register_and_login_test_user(client):
    client.post(
        "/register",
        json={
            "username": "calcuser",
            "email": "calc@example.com",
            "password": "Password123",
        },
    )

    login_response = client.post(
        "/login",
        json={
            "email": "calc@example.com",
            "password": "Password123",
        },
    )

    assert login_response.status_code == 200

    token = login_response.json()["access_token"]

    return {
        "Authorization": f"Bearer {token}"
    }


def test_create_calculation(client):
    headers = register_and_login_test_user(client)

    response = client.post(
        "/calculations",
        json={
            "a": 10,
            "b": 5,
            "type": "Add",
        },
        headers=headers,
    )

    assert response.status_code == 201

    data = response.json()

    assert data["a"] == 10
    assert data["b"] == 5
    assert data["type"] == "Add"
    assert data["result"] == 15
    assert data["user_id"] is not None


def test_browse_calculations(client):
    headers = register_and_login_test_user(client)

    client.post(
        "/calculations",
        json={
            "a": 8,
            "b": 2,
            "type": "Divide",
        },
        headers=headers,
    )

    response = client.get(
        "/calculations",
        headers=headers,
    )

    assert response.status_code == 200

    data = response.json()

    assert len(data) == 1
    assert data[0]["result"] == 4
    assert data[0]["type"] == "Divide"


def test_read_calculation(client):
    headers = register_and_login_test_user(client)

    create_response = client.post(
        "/calculations",
        json={
            "a": 9,
            "b": 3,
            "type": "Multiply",
        },
        headers=headers,
    )

    calculation_id = create_response.json()["id"]

    response = client.get(
        f"/calculations/{calculation_id}",
        headers=headers,
    )

    assert response.status_code == 200

    data = response.json()

    assert data["id"] == calculation_id
    assert data["result"] == 27


def test_update_calculation(client):
    headers = register_and_login_test_user(client)

    create_response = client.post(
        "/calculations",
        json={
            "a": 10,
            "b": 5,
            "type": "Add",
        },
        headers=headers,
    )

    calculation_id = create_response.json()["id"]

    response = client.put(
        f"/calculations/{calculation_id}",
        json={
            "a": 20,
            "b": 4,
            "type": "Multiply",
        },
        headers=headers,
    )

    assert response.status_code == 200

    data = response.json()

    assert data["a"] == 20
    assert data["b"] == 4
    assert data["type"] == "Multiply"
    assert data["result"] == 80


def test_delete_calculation(client):
    headers = register_and_login_test_user(client)

    create_response = client.post(
        "/calculations",
        json={
            "a": 15,
            "b": 5,
            "type": "Sub",
        },
        headers=headers,
    )

    calculation_id = create_response.json()["id"]

    delete_response = client.delete(
        f"/calculations/{calculation_id}",
        headers=headers,
    )

    assert delete_response.status_code == 200
    assert delete_response.json() == {
        "message": "Calculation deleted successfully"
    }

    get_response = client.get(
        f"/calculations/{calculation_id}",
        headers=headers,
    )

    assert get_response.status_code == 404
    assert (
        get_response.json()["error"]
        == "Calculation not found"
    )


def test_read_nonexistent_calculation(client):
    headers = register_and_login_test_user(client)

    response = client.get(
        "/calculations/999",
        headers=headers,
    )

    assert response.status_code == 404
    assert (
        response.json()["error"]
        == "Calculation not found"
    )


def test_update_nonexistent_calculation(client):
    headers = register_and_login_test_user(client)

    response = client.put(
        "/calculations/999",
        json={
            "a": 2,
            "b": 3,
            "type": "Add",
        },
        headers=headers,
    )

    assert response.status_code == 404
    assert (
        response.json()["error"]
        == "Calculation not found"
    )


def test_delete_nonexistent_calculation(client):
    headers = register_and_login_test_user(client)

    response = client.delete(
        "/calculations/999",
        headers=headers,
    )

    assert response.status_code == 404
    assert (
        response.json()["error"]
        == "Calculation not found"
    )


def test_divide_by_zero_is_rejected(client):
    headers = register_and_login_test_user(client)

    response = client.post(
        "/calculations",
        json={
            "a": 10,
            "b": 0,
            "type": "Divide",
        },
        headers=headers,
    )

    assert response.status_code == 400
    assert "Cannot divide by zero" in response.json()["error"]


def test_invalid_calculation_type_is_rejected(client):
    headers = register_and_login_test_user(client)

    response = client.post(
        "/calculations",
        json={
            "a": 10,
            "b": 5,
            "type": "Power",
        },
        headers=headers,
    )

    assert response.status_code == 400
    assert "type" in response.json()["error"]


def test_unauthorized_calculation_access(client):
    response = client.get("/calculations")

    assert response.status_code == 401