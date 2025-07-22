"""Repository module for managing user accounts using SQLAlchemy."""

from uuid import UUID

from sqlalchemy import Engine, String, create_engine
from sqlalchemy.orm import DeclarativeBase, Mapped, Session, mapped_column

from hello_sql_alchemy.models import User


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
        cls.engine = create_engine("sqlite:///example.db", echo=True)
        Base.metadata.create_all(cls.engine)  # Example connection string

    @classmethod
    def add_user(cls, user: User) -> None:
        """Add a new user to the repository."""
        with Session(cls.engine) as session:
            user_dao = UserDAO(id=user.id, name=user.name, fullname=user.fullname)
            session.add(user_dao)
            session.commit()

    @classmethod
    def get_user(cls, user_id: UUID) -> User | None:
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
    def list_users(cls) -> list[User]:
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
