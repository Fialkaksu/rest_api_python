"""User Service. Contains functions for interacting with the User table in the database."""

from sqlalchemy.ext.asyncio import AsyncSession
from libgravatar import Gravatar

from src.repository.users import UserRepository
from src.schemas import UserCreate


class UserService:
    """User Service."""

    def __init__(self, db: AsyncSession):
        """
        Initialize a UserService.

        Args:
            db: An AsyncSession object connected to the database.
        """
        self.repository = UserRepository(db)

    async def create_user(self, body: UserCreate):
        """
        Create a new User with the given attributes.

        Args:
            body (UserCreate): A UserCreate with the attributes to assign to the User.

        Returns:
            A User with the assigned attributes.
        """
        avatar = None
        try:
            g = Gravatar(body.email)
            avatar = g.get_image()
        except Exception as e:
            print(e)

        return await self.repository.create_user(body, avatar)

    async def get_user_by_id(self, user_id: int):
        """
        Get a User by its id.

        Args:
            user_id (int): The id of the User to retrieve.

        Returns:
            The User with the specified id, or None if no such User exists.
        """
        return await self.repository.get_user_by_id(user_id)

    async def get_user_by_username(self, username: str):
        """
        Get a User by its username.

        Args:
            username (str): The username of the User to retrieve.

        Returns:
            The User with the specified username, or None if no such User exists.
        """
        return await self.repository.get_user_by_username(username)

    async def get_user_by_email(self, email: str):
        """
        Get a User by its email.

        Args:
            email (str): The email of the User to retrieve.

        Returns:
            The User with the specified email, or None if no such User exists.
        """
        return await self.repository.get_user_by_email(email)

    async def confirmed_email(self, email: str):
        """
        Set a User's confirmed status to True.

        Args:
            email (str): The email of the User to update.

        Returns:
            None
        """
        return await self.repository.confirmed_email(email)

    async def update_avatar_url(self, email: str, url: str):
        """
        Update a User's avatar URL.

        Args:
            email (str): The email of the User to update.
            url (str): The new avatar URL.

        Returns:
            The updated User.
        """
        return await self.repository.update_avatar_url(email, url)
