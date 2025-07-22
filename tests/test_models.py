"""Test models for hello_sql_alchemy."""
from uuid import uuid4

from hello_sql_alchemy.models.user import User


def test_user() -> None:
    """Test creating a user."""
    user = User(name="testuser", fullname="Test User")

    assert user.name == "testuser"
    assert user.fullname == "Test User"
    assert user.id is not None  # Ensure ID is generated

def test_user_save() -> None:
    """Test saving a user."""
    user = User(name="testuser", fullname="Test User")
    user.save()

    # Check if the user is saved correctly
    retrieved_user = User.get(user.id)
    assert retrieved_user is not None
    assert retrieved_user.name == "testuser"
    assert retrieved_user.fullname == "Test User"

def test_user_list() -> None:
    """Test listing users."""
    expected_number_of_users = 2

    user1 = User(name="user1", fullname="User One")
    user1.save()

    user2 = User(name="user2", fullname="User Two")
    user2.save()

    users = User.list()
    assert len(users) >= expected_number_of_users # Ensure at least two users are listed
    assert any(u.name == "user1" for u in users)
    assert any(u.name == "user2" for u in users)


def test_user_get() -> None:
    """Test getting a user by ID."""
    user = User(name="testuser", fullname="Test User")
    user.save()

    retrieved_user = User.get(user.id)
    assert retrieved_user is not None
    assert retrieved_user.id == user.id
    assert retrieved_user.name == "testuser"
    assert retrieved_user.fullname == "Test User"

    # Test getting a non-existent user
    non_existent_user = User.get(uuid4())
    assert non_existent_user is None
