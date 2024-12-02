"""Contact service. Contains functions for interacting with the Contact table in the database."""

from fastapi import HTTPException, status
from sqlalchemy.ext.asyncio import AsyncSession

from src.database.models import User
from src.repository.contacts import ContactRepository
from src.schemas import ContactModel


class ContactService:
    """
    Service for interacting with the Contact table in the database.
    """

    def __init__(self, db: AsyncSession):
        """
        Initialize a ContactService.

        Args:
            db: An AsyncSession object connected to the database.
        """
        self.repository = ContactRepository(db)

    async def create_contact(self, body: ContactModel, user: User):
        """
        Create a new Contact with the given attributes.

        Args:
            body (ContactModel): A ContactModel with the attributes to assign to the Contact.
            user (User): The User who owns the Contact.

        Returns:
            A Contact with the assigned attributes.
        """
        if await self.repository.is_contact_exists(body.email, body.phone_number, user):
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail=f"Contact with '{body.email}' email or '{body.phone_number}' phone number already exists.",
            )
        return await self.repository.create_contact(body, user)

    async def get_contacts(
        self,
        first_name: str,
        last_name: str,
        email: str,
        skip: int,
        limit: int,
        user: User,
    ):
        """
        Get a list of Contacts owned by `user` with pagination.

        Args:
            first_name (str): The first name of the Contacts to retrieve.
            last_name (str): The last name of the Contacts to retrieve.
            email (str): The email of the Contacts to retrieve.
            skip (int): The number of Notes to skip.
            limit (int): The maximum number of Notes to return.
            user (User): The owner of the Notes to retrieve.

        Returns:
            A list of Contacts.
        """
        return await self.repository.get_contacts(
            first_name, last_name, email, skip, limit, user
        )

    async def get_contact(self, contact_id: int, user: User):
        """
        Get a Contact by its id.

        Args:
            contact_id (int): The id of the Contact to retrieve.
            user (User): The owner of the Contact to retrieve.

        Returns:
            The Contact with the specified id, or None if no such Contact exists.
        """
        return await self.repository.get_contact_by_id(contact_id, user)

    async def update_contact(self, contact_id: int, body: ContactModel, user: User):
        """
        Update a Contact with the given attributes.

        Args:
            contact_id (int): The id of the Contact to update.
            body (ContactModel): A ContactModel with the attributes to assign to the Contact.
            user (User): The User who owns the Contact.

        Returns:
            The updated Contact, or None if no Contact with the given id exists.
        """
        return await self.repository.update_contact(contact_id, body, user)

    async def remove_contact(self, contact_id: int, user: User):
        """
        Delete a Contact by its id.

        Args:
            contact_id (int): The id of the Contact to delete.
            user (User): The owner of the Contact to delete.

        Returns:
            The deleted Contact, or None if no Contact with the given id exists.
        """
        return await self.repository.remove_contact(contact_id, user)

    async def get_upcoming_birthdays(self, days: int, user: User):
        """
        Get a list of Contacts owned by `user` with pagination for upcoming birthdays.

        Args:
            days (int): The number of days in the future to check.
            user (User): The owner of the Contacts to check.

        Returns:
            A list of Contacts with upcoming birthdays.
        """
        return await self.repository.get_upcoming_birthdays(days, user)
