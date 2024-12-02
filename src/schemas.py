"""Schemas for pydantic models."""

from datetime import date, datetime
from typing import Optional
from pydantic import BaseModel, Field, ConfigDict, EmailStr


class ContactModel(BaseModel):
    """
    Contact model.

    Attributes:
        first_name (str): The first name of the contact.
        last_name (str): The last name of the contact.
        email (str): The email of the contact.
        phone_number (str): The phone number of the contact.
        birth_date (date): The birth date of the contact.
        info (Optional[str]): The additional information about the contact.
    """

    first_name: str = Field(min_length=2, max_length=50)
    last_name: str = Field(min_length=2, max_length=50)
    email: EmailStr = Field(min_length=7, max_length=100)
    phone_number: str = Field(min_length=7, max_length=20)
    birth_date: date
    info: Optional[str] = None


class ContactResponse(ContactModel):
    """
    Contact response model.

    Attributes:
        id (int): The id of the contact.
        created_at (datetime): The creation date of the contact.
        updated_at (Optional[datetime]): The last update date of the contact.
    """

    id: int
    created_at: datetime
    updated_at: Optional[datetime]

    model_config = ConfigDict(from_attributes=True)


class User(BaseModel):
    """
    User model.

    Attributes:
        id (int): The id of the user.
        username (str): The username of the user.
        email (str): The email of the user.
        avatar (str): The avatar of the user.
    """

    id: int
    username: str
    email: str
    avatar: str

    model_config = ConfigDict(from_attributes=True)


class UserCreate(BaseModel):
    """
    User create model.

    Attributes:
        username (str): The username of the user.
        email (str): The email of the user.
        password (str): The password of the user.
    """

    username: str
    email: str
    password: str


class Token(BaseModel):
    """
    Token model.

    Attributes:
        access_token (str): The access token of the user.
        token_type (str): The type of the token.
    """

    access_token: str
    token_type: str


class RequestEmail(BaseModel):
    """
    Request email model.

    Attributes:
        email (EmailStr): The email of the user.
    """

    email: EmailStr
