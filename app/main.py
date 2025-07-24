"""Main module to demonstrate SQLAlchemy and pydantic integration."""

import uuid

from fastapi import FastAPI, HTTPException

from .models import User
from .repository import Repository

api = FastAPI()


@api.get("/health", include_in_schema=False)
def health_check() -> dict:
    """Health check endpoint to verify the API is running.

    It will check the database schema version and return a simple status message.
    """
    Repository.create_engine()  # Initialize the repository engine
    current_revision = Repository.get_current_revision()
    if current_revision is None:
        raise HTTPException(status_code=500, detail="Database schema not initialized")
    return {"status": "ok", "currentDatabaseSchemaRevision": current_revision}


@api.get("/users")
def list_users() -> list[User]:
    """List all users."""
    return User.list()


@api.post("/users")
def create_user(user: User) -> User:
    """Create a new user."""
    user.save()
    return user


@api.get("/users/{user_id}")
def get_user(user_id: uuid.UUID) -> User:
    """Retrieve a user by ID."""
    user = User.get(user_id)
    if not user:
        raise HTTPException(status_code=404, detail="User not found")
    return user
