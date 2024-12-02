"""
Models for database.

Attributes:
- Base: Base class for declarative models.
- Contact: Contact model.
- User: User model.
"""

from datetime import datetime, date

from sqlalchemy import Integer, String, func, Column, ForeignKey
from sqlalchemy.orm import mapped_column, Mapped, DeclarativeBase, relationship
from sqlalchemy.sql.sqltypes import DateTime, Date, Boolean


class Base(DeclarativeBase):
    """
    Base class for all ORM models.

    This class uses SQLAlchemy's declarative base to provide the
    foundation for defining ORM models.
    """

    pass


class Contact(Base):
    """
    Contact model.

    Attributes:
        id (int): The id of the contact.
        first_name (str): The first name of the contact.
        last_name (str): The last name of the contact.
        email (str): The email of the contact.
        phone_number (str): The phone number of the contact.
        birth_date (date): The birth date of the contact.
        created_at (datetime): The creation date of the contact.
        updated_at (datetime): The last update date of the contact.
        user_id (int): The id of the user who owns the contact.
        user (User): The user who owns the contact.
        info (str): The additional information about the contact.
    """

    __tablename__ = "contacts"
    id: Mapped[int] = mapped_column(Integer, primary_key=True)
    first_name: Mapped[str] = mapped_column(String(50), nullable=False)
    last_name: Mapped[str] = mapped_column(String(50), nullable=False)
    email: Mapped[str] = mapped_column(String(100), nullable=False, unique=True)
    phone_number: Mapped[str] = mapped_column(String(20), nullable=False, unique=True)
    birth_date: Mapped[date] = mapped_column("birth_date", Date, nullable=False)
    created_at: Mapped[datetime] = mapped_column(
        "created_at", DateTime, default=func.now()
    )
    updated_at: Mapped[datetime] = mapped_column(
        "updated_at", DateTime, default=func.now(), onupdate=func.now()
    )
    user_id = Column(
        "user_id", ForeignKey("users.id", ondelete="CASCADE"), nullable=False
    )
    user = relationship("User", backref="contacts")
    info: Mapped[str] = mapped_column(String(500), nullable=True)


class User(Base):
    """
    User model.

    Attributes:
        id (int): The id of the user.
        username (str): The username of the user.
        email (str): The email of the user.
        hashed_password (str): The hashed password of the user.
        created_at (datetime): The creation date of the user.
        avatar (str): The avatar of the user.
        confirmed (bool): The confirmation status of the user.
    """

    __tablename__ = "users"
    id = Column(Integer, primary_key=True)
    username = Column(String, unique=True)
    email = Column(String, unique=True)
    hashed_password = Column(String)
    created_at = Column(DateTime, default=func.now())
    avatar = Column(String(255), nullable=True)
    confirmed = Column(Boolean, default=False)
