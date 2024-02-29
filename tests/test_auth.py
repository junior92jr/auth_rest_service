from tests.config import get_testing_client


client = get_testing_client()


def test_recover_password_success() -> None:
    """Test recover password."""

    response = client.post(
        "/auth/recover-password",
        headers={"client-version": "3.3.1"},
        json={
            "recovery_code": 1631959404,
            "email": "sbahtgijwovhje@gmail.com",
            "password": "password123"
        }
    )

    json_response = response.json()
    expected_detail = "New Credentials Created for sbahtgijwovhje@gmail.com."

    assert response.status_code == 200
    assert json_response.get('message') == expected_detail


def test_recover_password_invalid_header() -> None:
    """Test recover password with invalid header."""

    response = client.post(
        "/auth/recover-password",
        headers={"client-version": "dasdas"},
        json={
            "recovery_code": 1631959404,
            "email": "sbahtgijwovhje@gmail.com",
            "password": "password123"
        }
    )

    json_response = response.json()
    expected_detail = "Header app-version 'dasdas' is not valid."

    assert response.status_code == 422
    assert json_response["detail"] == expected_detail

    response = client.post(
        "/auth/recover-password",
        headers={"client-version": "1"},
        json={
            "recovery_code": 1631959404,
            "email": "sbahtgijwovhje@gmail.com",
            "password": "password123"
        }
    )

    json_response = response.json()
    expected_detail = "Header app-version '1' is lower than 2.1.0."

    assert response.status_code == 422
    assert json_response["detail"] == expected_detail


def test_invalid_authentication() -> None:
    """Test invalid authentication."""

    response = client.post(
        "/auth/login",
        headers={"client-version": "3"},
        data={
            "username": "sbahtgijw2ovhje@gmail.com",
            "password": "password123"
        }
    )

    json_response = response.json()
    expected_detail = "Incorrect username or password"

    assert response.status_code == 401
    assert json_response["detail"] == expected_detail


def test_authenticated_reset_password() -> None:
    """Test authentication with header."""

    response = client.post(
        "/auth/recover-password",
        headers={"client-version": "3.3.1"},
        json={
            "recovery_code": 1631959404,
            "email": "sbahtgijwovhje@gmail.com",
            "password": "password123"
        }
    )

    response = client.post(
        "/auth/login",
        headers={"client-version": "3.2.1"},
        data={
            "username": "sbahtgijwovhje@gmail.com",
            "password": "password123"
        }
    )

    json_response = response.json()

    assert response.status_code == 200
    assert json_response["token_type"] == "bearer"

    assert "access_token" in json_response
    assert "token_type" in json_response

    access_token = json_response["access_token"]

    response = client.post(
        "/auth/reset-password",
        headers={
            "client-version": "3.2.1",
            "Authorization": f"Bearer {access_token}"
        },
        json={
            "old_password": "password123",
            "new_password": "password321"
        }
    )

    json_response = response.json()

    assert response.status_code == 200
    expected_detail = "New Credentials Created for sbahtgijwovhje@gmail.com."
    assert json_response["message"] == expected_detail
