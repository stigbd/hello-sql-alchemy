"""Test repository for nrl_sdk_lib."""

import os
from http import HTTPStatus
from pathlib import Path
from typing import Any

import httpx
import pytest

DATABASE_HOST = os.getenv("DATABASE_HOST")
DATABASE_PORT = int(os.getenv("DATABASE_PORT", "5432"))
DATABASE_NAME = os.getenv("DATABASE_NAME")
DATABASE_USER = os.getenv("DATABASE_USER")
DATABASE_PASSWORD = os.getenv("DATABASE_PASSWORD")
DATABASE_URL = f"postgresql+psycopg://{DATABASE_USER}:{DATABASE_PASSWORD}@{DATABASE_HOST}:{DATABASE_PORT}/{DATABASE_NAME}"


def is_responsive(url: str) -> bool | None:
    """Check if postgresql is ready."""
    try:
        response = httpx.get(f"{url}/health", timeout=30)
        if response.status_code == HTTPStatus.OK:
            return True
    except ConnectionError:
        return False
    return False


@pytest.fixture(scope="session")
def http_service(docker_ip: str, docker_services: Any) -> str:
    """Ensure that HTTP service is up and responsive."""
    # `port_for` takes a container port and returns the corresponding host port
    port = docker_services.port_for("api", 8000)
    url = f"http://{docker_ip}:{port}"
    docker_services.wait_until_responsive(
        timeout=30.0, pause=0.1, check=lambda: is_responsive(url)
    )
    return url


@pytest.fixture(scope="session")
def docker_compose_file(pytestconfig: Any) -> Any:
    """Override default location of docker-compose.yml file."""
    return Path(str(pytestconfig.rootdir), "compose.yaml")


@pytest.fixture(scope="session")
def docker_setup() -> Any:
    """Make sure to run the database migrations before starting the tests."""
    return ["up --build -d", "exec api uv run alembic upgrade head"]


@pytest.fixture(scope="session")
def docker_cleanup() -> Any:
    """Override default test clean-up action."""
    return "stop"


def test_create_user(http_service: str) -> None:
    """Should create a user and return the user ID."""
    url = f"{http_service}/users"
    user_data = {"name": "testuser", "fullname": "Test User"}
    response = httpx.post(url, json=user_data)
    assert response.status_code == HTTPStatus.OK, (
        f"Failed to create user: {response.text}"
    )

    user = response.json()
    assert "id" in user, "Response should contain 'id' field"
    assert user["name"] == user_data["name"], "User name should match"
    assert user["fullname"] == user_data["fullname"], "User fullname should match"


def test_get_user_list(http_service: str) -> None:
    """Should return a list of one user."""
    url = f"{http_service}/users"
    response = httpx.get(url)
    assert response.status_code == HTTPStatus.OK, (
        f"Failed to get user list: {response.text}"
    )

    users = response.json()
    assert isinstance(users, list), "Response should be a list"
    assert len(users) >= 1, "There should be at least one user in the list"
    assert "id" in users[0], "User should have an 'id' field"
    assert "name" in users[0], "User should have a 'name' field"
    assert "fullname" in users[0], "User should have a 'fullname' field"
