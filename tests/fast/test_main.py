"""Test models."""

from http import HTTPStatus
from uuid import UUID, uuid4

import pytest
from fastapi.testclient import TestClient
from pytest_mock import MockFixture

from app import api
from app.models.user import User


@pytest.fixture
def client() -> TestClient:
    """Fixture to create a test client for the FastAPI application."""
    return TestClient(api)


def test_health_check(client: TestClient, mocker: MockFixture) -> None:
    """Health check endpoint should return status OK."""
    current_database_schema_revision = "revision_1"
    current_head = "revision_1"
    mocker.patch(
        "app.repository.Repository.get_current_revision",
        return_value=current_database_schema_revision,
    )
    mocker.patch("app.repository.Repository.check", return_value=True)
    mocker.patch(
        "app.repository.Repository.get_current_head", return_value=current_head
    )

    response = client.get("/health")
    assert response.status_code == HTTPStatus.OK, (
        f"Health check failed: {response.text}"
    )
    assert response.json() == {
        "status": "ok",
        "currentDatabaseSchemaRevision": current_database_schema_revision,
        "currentHead": current_head,
    }, "Health check response should be 'ok'"


def test_health_check_no_revision(client: TestClient, mocker: MockFixture) -> None:
    """Health check endpoint should return 500 if no revision is found."""
    current_database_schema_revision = None
    current_head = "revision_1"

    mocker.patch(
        "app.repository.Repository.get_current_revision",
        return_value=current_database_schema_revision,
    )
    mocker.patch("app.repository.Repository.check", return_value=False)
    mocker.patch(
        "app.repository.Repository.get_current_head", return_value=current_head
    )

    response = client.get("/health")
    assert response.status_code == HTTPStatus.INTERNAL_SERVER_ERROR
    detail = response.json().get("detail", "")
    assert "Database schema not up to date." in detail
    assert (
        f"Current database schema revision is '{current_database_schema_revision}"
        in detail
    )
    assert f"and current head is '{current_head}'" in detail


def test_user_save(client: TestClient, mocker: MockFixture) -> None:
    """Should return the user with a valid uuid as id."""
    # Mock the database save method
    mocker.patch("app.repository.Repository.add_user", return_value=None)

    # Create a user instance
    user = {"name": "testuser", "fullname": "Test User"}
    response = client.post("/users", json=user)

    assert response.status_code == HTTPStatus.OK
    assert response.json()["name"] == user["name"]
    assert response.json()["fullname"] == user["fullname"]
    assert "id" in response.json(), "Response should contain 'id' field"
    assert isinstance(response.json()["id"], str), "ID should be a string (UUID)"
    assert UUID(response.json()["id"]), "ID should be a valid UUID"


def test_user_list(client: TestClient, mocker: MockFixture) -> None:
    """Should return a list of users."""
    expected_number_of_users = 2
    # Mock the database list method
    mocker.patch(
        "app.repository.Repository.list_users",
        return_value=[
            User(id=uuid4(), name="test1", fullname="Test One"),
            User(id=uuid4(), name="test2", fullname="Test Two"),
        ],
    )

    response = client.get("/users")

    assert response.status_code == HTTPStatus.OK, (
        f"Failed to get user list: {response.text}"
    )
    assert isinstance(response.json(), list), "Response should be a list"
    assert len(response.json()) == expected_number_of_users, (
        f"Expected {expected_number_of_users} users, got {len(response.json())}"
    )
    assert all("id" in user for user in response.json()), (
        "Each user should have an 'id' field"
    )
    assert all("name" in user for user in response.json()), (
        "Each user should have a 'name' field"
    )
    assert all("fullname" in user for user in response.json()), (
        "Each user should have a 'fullname' field"
    )


def test_user_get(client: TestClient, mocker: MockFixture) -> None:
    """Should return a specific user."""
    # Mock the database get method
    user_id = uuid4()

    mocker.patch(
        "app.repository.Repository.get_user",
        return_value=User(name="testuser", fullname="Test User", id=user_id),
    )

    response = client.get(f"/users/{user_id}")
    assert response.status_code == HTTPStatus.OK, f"Failed to get user: {response.text}"
    retrieved_user = response.json()

    assert retrieved_user is not None
    assert retrieved_user["id"] == str(user_id)
    assert retrieved_user["name"] == "testuser"
    assert retrieved_user["fullname"] == "Test User"


def test_user_get_not_found(client: TestClient, mocker: MockFixture) -> None:
    """Should return 404 Not Found for non-existing user."""
    user_id = uuid4()
    mocker.patch("app.repository.Repository.get_user", return_value=None)

    response = client.get(f"/users/{user_id}")
    assert response.status_code == HTTPStatus.NOT_FOUND, (
        f"Expected 404 Not Found, got {response.status_code}: {response.text}"
    )
    assert response.json() == {"detail": "User not found"}, (
        "Response should indicate that the user was not found"
    )
