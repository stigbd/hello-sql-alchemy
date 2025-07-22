"""User model for the application."""

from typing import Union
from uuid import UUID, uuid4

from pydantic import BaseModel, Field


class User(BaseModel):
    """A user model."""

    name: str
    fullname: str
    id: UUID = Field(default_factory=uuid4)

    def save(self) -> None:
        """Simulate saving the user to a database."""
        # lazy import to avoid circular dependencies:
        from hello_sql_alchemy.repository import Repository  # noqa: PLC0415

        repository = Repository()
        repository.create_engine()
        # Create the repository and initialize the database connection.
        repository.add_user(self)


    @classmethod
    def list(cls) -> list["User"]:
        """List all users."""
        # lazy import to avoid circular dependencies:
        from hello_sql_alchemy.repository import Repository  # noqa: PLC0415

        repository = Repository()
        repository.create_engine()

        return repository.list_users()

    @classmethod
    def get(cls, user_id: UUID) -> Union[None, "User"]:
        """Get a user by ID."""
        # lazy import to avoid circular dependencies:
        from hello_sql_alchemy.repository import Repository  # noqa: PLC0415

        repository = Repository()
        repository.create_engine()
        user = repository.get_user(user_id)
        if user:
            return user
        return None
