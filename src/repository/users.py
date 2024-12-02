"""
Module for interacting with the User table in the database.
"""

from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession

from src.database.models import User
from src.schemas import UserCreate


class UserRepository:
    """
    A class that provides methods for interacting with the User table in the database.

    Attributes:
        db (AsyncSession): An AsyncSession object connected to the database.

    Methods:
        get_user_by_id: Get a User by its id.
        get_user_by_username: Get a User by its username.
        get_user_by_email: Get a User by its email.
        create_user: Create a new User with the given attributes.
        confirmed_email: Set a User's confirmed status to True.
        update_avatar_url: Update a User's avatar URL.
    """

    def __init__(self, session: AsyncSession):
        """
        Initialize a UserRepository.

        Args:
            session: An AsyncSession object connected to the database.
        """
        self.db = session

    async def get_user_by_id(self, user_id: int) -> User | None:
        """
        Get a User by its id.

        Args:
            user_id: The id of the User to retrieve.

        Returns:
            The User with the specified id, or None if no such User exists.
        """
        stmt = select(User).filter_by(id=user_id)
        user = await self.db.execute(stmt)
        return user.scalar_one_or_none()

    async def get_user_by_username(self, username: str) -> User | None:
        """
        Get a User by its username.

        Args:
            username: The username of the User to retrieve.

        Returns:
            The User with the specified username, or None if no such User exists.
        """
        stmt = select(User).filter_by(username=username)
        user = await self.db.execute(stmt)
        return user.scalar_one_or_none()

    async def get_user_by_email(self, email: str) -> User | None:
        """
        Get a User by its email.

        Args:
            email: The email of the User to retrieve.

        Returns:
            The User with the specified email, or None if no such User exists.
        """
        stmt = select(User).filter_by(email=email)
        user = await self.db.execute(stmt)
        return user.scalar_one_or_none()

    async def create_user(self, body: UserCreate, avatar: str = None) -> User:
        """
        Create a new User with the given attributes.

        Args:
            body: The attributes of the User to create.
            avatar: The avatar of the User to create.

        Returns:
            The created User.
        """
        user = User(
            **body.model_dump(exclude_unset=True, exclude={"password"}),
            hashed_password=body.password,
            avatar=avatar
        )
        self.db.add(user)
        await self.db.commit()
        await self.db.refresh(user)
        return user

    async def confirmed_email(self, email: str) -> None:
        """
        Set a User's confirmed status to True.

        Args:
            email: The email of the User to update.

        Returns:
            None
        """
        user = await self.get_user_by_email(email)
        user.confirmed = True
        await self.db.commit()

    async def update_avatar_url(self, email: str, url: str) -> User:
        """
        Update a User's avatar URL.

        Args:
            email: The email of the User to update.
            url: The new avatar URL.

        Returns:
            The updated User.
        """
        user = await self.get_user_by_email(email)
        user.avatar = url
        await self.db.commit()
        await self.db.refresh(user)
        return user
