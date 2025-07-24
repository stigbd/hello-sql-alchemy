"""Repository module for managing user accounts using SQLAlchemy."""

import os
from uuid import UUID

from sqlalchemy import Engine, String, create_engine
from sqlalchemy.orm import DeclarativeBase, Mapped, Session, mapped_column

from alembic.migration import MigrationContext
from app.models import User

DATABASE_HOST = os.getenv("DATABASE_HOST")
DATABASE_PORT = int(os.getenv("DATABASE_PORT", "5432"))
DATABASE_NAME = os.getenv("DATABASE_NAME")
DATABASE_USER = os.getenv("DATABASE_USER")
DATABASE_PASSWORD = os.getenv("DATABASE_PASSWORD")
DATABASE_URL = f"postgresql+psycopg://{DATABASE_USER}:{DATABASE_PASSWORD}@{DATABASE_HOST}:{DATABASE_PORT}/{DATABASE_NAME}"


class Base(DeclarativeBase):
    """Base class for SQLAlchemy models."""


class UserDAO(Base):
    """Data Access Object for User entity."""

    __tablename__ = "user_account"
    id: Mapped[UUID] = mapped_column(primary_key=True)
    name: Mapped[str] = mapped_column(String(30))
    fullname: Mapped[str | None]


class Repository:
    """Repository for managing user accounts."""

    engine: Engine

    @classmethod
    def create_engine(cls) -> None:
        """Initialize the repository with a SQLAlchemy session."""
        cls.engine = create_engine(DATABASE_URL, echo=True)

    @classmethod
    def get_current_revision(cls) -> str | None:  # pragma: no cover
        """Get the current database schema revision."""
        # This method should return the current revision of the database schema.
        conn = cls.engine.connect()
        context = MigrationContext.configure(conn)
        current_rev = context.get_current_revision()
        conn.close()
        return current_rev

    @classmethod
    def add_user(cls, user: User) -> None:
        """Add a new user to the repository."""
        with Session(cls.engine) as session:  # pragma: no cover
            user_dao = UserDAO(id=user.id, name=user.name, fullname=user.fullname)
            session.add(user_dao)
            session.commit()

    @classmethod
    def get_user(cls, user_id: UUID) -> User | None:  # pragma: no cover
        """Retrieve a user by ID."""
        session = Session(cls.engine)
        user_dao = session.query(UserDAO).filter(UserDAO.id == user_id).first()
        if user_dao:
            return User(
                id=user_dao.id,
                name=user_dao.name,
                fullname=user_dao.fullname if user_dao.fullname else "",
            )
        return None

    @classmethod
    def list_users(cls) -> list[User]:  # pragma: no cover
        """List all users in the repository."""
        session = Session(cls.engine)
        return [
            User(
                id=user_dao.id,
                name=user_dao.name,
                fullname=user_dao.fullname if user_dao.fullname else "",
            )
            for user_dao in session.query(UserDAO).all()
        ]
