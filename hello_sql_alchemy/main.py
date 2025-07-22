"""Main module to demonstrate SQLAlchemy and pydantic integration."""

from .models import User


def main() -> None:
    """Demonstrate use of SQLAlchemy and pydantic."""
    john = User(
        name="johndoe",
        fullname="John Doe",
    )

    john.save()

    jane = User(name="janedoe", fullname="Jane Doe")
    jane.save()

    users = User.list()
    for user in users:
        print(f"User ID: {user.id}, Name: {user.name}, Fullname: {user.fullname}")  # noqa: T201

    user = User.get(jane.id)
    if user:
        print(f"Retrieved User: {user.name} with ID {user.id}")  # noqa: T201
    else: # pragma: no cover
        print("User not found.")  # noqa: T201
