import pytest
from fastapi import status
from sqlmodel import Session
from fastapi.testclient import TestClient
from .conftest import AUTH_PREFIX
from auth.models import User
from auth.services import UserService
from auth.utils import verify_password


@pytest.mark.skip
def test_create_account(client: TestClient, session: Session):
    request_data = {
        "username": "username",
        "password": "password",
        "email": "email@example.com",
    }

    response = client.post(f"{AUTH_PREFIX}/signup", json=request_data)
    response_data = response.json()
    user_data = response_data["user"]

    created_user = UserService().get_by_id(session, user_data["id"])

    assert response.status_code == status.HTTP_201_CREATED
    assert request_data["username"] == user_data["username"]
    assert verify_password(request_data["password"], created_user.password)
    assert request_data["email"] == user_data["email"]


def test_verify_email_account(
    client: TestClient,
    session: Session,
    signup_user: User,
    url_safe_token: str,
):
    response = client.get(f"{AUTH_PREFIX}/verify/{url_safe_token}")

    session.refresh(signup_user)

    assert response.status_code == status.HTTP_200_OK
    assert signup_user.is_verified == True


def test_login(client: TestClient, signup_user: User):
    request_data = {"username": "username", "password": "password"}
    response = client.post(f"{AUTH_PREFIX}/signin", json=request_data)
    response_data = response.json()

    assert response.status_code == status.HTTP_200_OK
    assert response_data.get("access_token") is not None
    assert response_data.get("refresh_token") is not None


def test_refresh_token(client: TestClient, signin_user: User):
    request_header = {"Authorization": f"Bearer {signin_user["refresh_token"]}"}
    response = client.get(f"{AUTH_PREFIX}/refresh_token", headers=request_header)
    response_data = response.json()

    assert response.status_code == status.HTTP_200_OK
    assert response_data.get("access_token") is not None


def test_logout(client: TestClient, signin_user: User):
    request_header = {"Authorization": f"Bearer {signin_user["access_token"]}"}
    response = client.get(f"{AUTH_PREFIX}/logout", headers=request_header)

    assert response.status_code == status.HTTP_200_OK


@pytest.mark.skip
def test_request_password_reset(client: TestClient):
    request_data = {"email": "email@example.com"}
    response = client.post(f"{AUTH_PREFIX}/request_password_reset", json=request_data)

    assert response.status_code == status.HTTP_200_OK


def test_reset_password(
    client: TestClient,
    session: Session,
    signup_user: User,
    url_safe_token: str,
):
    request_data = {"new_password": "test", "confirm_password": "test"}
    response = client.post(
        f"{AUTH_PREFIX}/reset_password/{url_safe_token}", json=request_data
    )

    session.refresh(signup_user)

    assert response.status_code == status.HTTP_200_OK
    assert verify_password(request_data["new_password"], signup_user.password)
