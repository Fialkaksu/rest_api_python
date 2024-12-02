"""
Auth service. Contains functions for user authentication and registration.

Classes:
- Hash: A class for password hashing and verification.

Functions:
- create_access_token(data: dict, expires_delta: Optional[int] = None): Generates a new access token.
- get_current_user(token: str = Depends(oauth2_scheme)): Retrieves the current user based on the provided token.
- create_email_token(data: dict): Generates a token for email verification.
- create_email_token(data: dict): Generates a token for email verification.
"""

from datetime import datetime, timedelta, timezone
from typing import Optional

from fastapi import Depends, HTTPException, status
from passlib.context import CryptContext
from fastapi.security import OAuth2PasswordBearer
from sqlalchemy.ext.asyncio import AsyncSession
from jose import JWTError, jwt

from src.database.db import get_db
from src.conf.config import settings
from src.services.users import UserService


class Hash:
    """A class for password hashing and verification."""

    pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")

    def verify_password(self, plain_password, hashed_password):
        """
        Verifies a plain password against a hashed password.

        Args:
            plain_password (str): The plain text password to verify.
            hashed_password (str): The hashed password to compare against.

        Returns:
            True if the plain password matches the hashed password, False otherwise.
        """
        return self.pwd_context.verify(plain_password, hashed_password)

    def get_password_hash(self, password: str):
        """
        Generates a hashed password from a plain text password.

        Args:
            password (str): The plain text password to hash.

        Returns:
            The hashed password as a string.
        """
        return self.pwd_context.hash(password)


oauth2_scheme = OAuth2PasswordBearer(tokenUrl="/api/auth/login")


# define a function to generate a new access token
async def create_access_token(data: dict, expires_delta: Optional[int] = None):
    """
    Generates a new access token.

    Args:
        data (dict): A dictionary of data to include in the token.
        expires_delta (Optional[int]): The number of seconds until the token expires. Defaults to None.

    Returns:
        A JWT token as a string.
    """
    to_encode = data.copy()
    if expires_delta:
        expire = datetime.now(timezone.utc) + timedelta(seconds=expires_delta)
    else:
        expire = datetime.now(timezone.utc) + timedelta(
            seconds=settings.JWT_EXPIRATION_SECONDS
        )
    to_encode.update({"exp": expire})
    encoded_jwt = jwt.encode(
        to_encode, settings.JWT_SECRET, algorithm=settings.JWT_ALGORITHM
    )
    return encoded_jwt


async def get_current_user(
    token: str = Depends(oauth2_scheme), db: AsyncSession = Depends(get_db)
):
    """
    Retrieves the current user based on the provided token.

    Args:
        token (str): The JWT token to retrieve the user from.
        db (AsyncSession): The database session to use.

    Returns:
        The user object associated with the provided token.

    Raises:
        HTTPException: If the token is invalid or the user is not found.
    """
    credentials_exception = HTTPException(
        status_code=status.HTTP_401_UNAUTHORIZED,
        detail="Could not validate credentials",
        headers={"WWW-Authenticate": "Bearer"},
    )

    try:
        # Decode JWT
        payload = jwt.decode(
            token, settings.JWT_SECRET, algorithms=[settings.JWT_ALGORITHM]
        )
        username = payload["sub"]
        if username is None:
            raise credentials_exception
    except JWTError as e:
        raise credentials_exception
    user_service = UserService(db)
    user = await user_service.get_user_by_username(username)
    if user is None:
        raise credentials_exception
    return user


def create_email_token(data: dict):
    """
    Generates a token for email verification.

    Args:
        data (dict): A dictionary of data to include in the token.

    Returns:
        A JWT token as a string.
    """
    to_encode = data.copy()
    expire = datetime.now(timezone.utc) + timedelta(days=7)
    to_encode.update({"iat": datetime.now(timezone.utc), "exp": expire})
    token = jwt.encode(to_encode, settings.JWT_SECRET, algorithm=settings.JWT_ALGORITHM)
    return token


async def get_email_from_token(token: str):
    """
    Retrieves the email address from a JWT token.

    Args:
        token (str): The JWT token to decode.

    Returns:
        The email address associated with the token.

    Raises:
        HTTPException: If the token is invalid.
    """
    try:
        payload = jwt.decode(
            token, settings.JWT_SECRET, algorithms=[settings.JWT_ALGORITHM]
        )
        email = payload["sub"]
        return email
    except JWTError as e:
        raise HTTPException(
            status_code=status.HTTP_422_UNPROCESSABLE_ENTITY,
            detail="Неправильний токен для перевірки електронної пошти",
        )
