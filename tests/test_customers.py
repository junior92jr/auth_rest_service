from tests.config import get_testing_client


client = get_testing_client()


def test_unauthorised_customer_request() -> None:
    """Test unauthorised customer endpoint request."""

    response = client.get(
        "/customers/me",
        headers={
            "client-version": "3.2.1"
        }
    )

    assert response.status_code == 401


def test_customer_authenticated_endpoint() -> None:
    """Test me endpoint from customers."""

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
    access_token = json_response["access_token"]

    response = client.get(
        "/customers/me",
        headers={
            "client-version": "3.2.1",
            "Authorization": f"Bearer {access_token}"
        }
    )

    json_response = response.json()

    assert response.status_code == 200

    assert "customer_id" in json_response
    assert "email" in json_response
    assert "country" in json_response
    assert "language" in json_response
 