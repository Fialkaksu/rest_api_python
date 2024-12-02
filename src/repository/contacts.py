"""
Module for interacting with the Contact table in the database.
"""

from datetime import date, timedelta
from typing import List

from sqlalchemy import select, func, and_, or_
from sqlalchemy.ext.asyncio import AsyncSession

from src.database.models import Contact, User
from src.schemas import ContactModel


class ContactRepository:
    """
    A class that provides methods for interacting with the Contact table in the database.

    Attributes:
        db (AsyncSession): An AsyncSession object connected to the database.

    Methods:
        get_contacts: Get a list of Contacts owned by `user` with pagination.
        get_contact_by_id: Get a Contact by its id.
        create_contact: Create a new Contact with the given attributes.
        update_contact: Update a Contact with the given attributes.
        remove_contact: Delete a Contact by its id.
        is_contact_exists: Check if a Contact with the given attributes already exists.
    """

    def __init__(self, session: AsyncSession):
        """
        Initialize a ContactRepository.

        Args:
            session: An AsyncSession object connected to the database.
        """
        self.db = session

    async def get_contacts(
        self,
        first_name: str,
        last_name: str,
        email: str,
        skip: int,
        limit: int,
        user: User,
    ) -> List[Contact]:
        """
        Get a list of Contacts owned by `user` with pagination.

        Args:
            first_name: The first name of the Contacts to retrieve.
            last_name: The last name of the Contacts to retrieve.
            email: The email of the Contacts to retrieve.
            skip: The number of Notes to skip.
            limit: The maximum number of Notes to return.
            user: The owner of the Notes to retrieve.

        Returns:
            A list of Contacts.
        """
        stmt = (
            select(Contact)
            .filter_by(user=user)
            .where(Contact.first_name.contains(first_name))
            .where(Contact.last_name.contains(last_name))
            .where(Contact.email.contains(email))
            .offset(skip)
            .limit(limit)
        )
        contacts = await self.db.execute(stmt)
        return contacts.scalars().all()

    async def get_contact_by_id(self, contact_id: int, user: User) -> Contact | None:
        """
        Get a Contact by its id.

        Args:
            contact_id: The id of the Note to retrieve.
            user: The owner of the Contact to retrieve.

        Returns:
            The Contact with the specified id, or None if no such Contact exists.
        """
        stmt = select(Contact).filter_by(id=contact_id, user=user)
        contact = await self.db.execute(stmt)
        return contact.scalar_one_or_none()

    async def create_contact(self, body: ContactModel, user: User) -> Contact:
        """
        Create a new Contact with the given attributes.

        Args:
            body: A ContactModel with the attributes to assign to the Contact.
            user: The User who owns the Contact.

        Returns:
            A Contact with the assigned attributes.
        """
        contact = Contact(**body.model_dump(exclude_unset=True), user=user)
        self.db.add(contact)
        await self.db.commit()
        await self.db.refresh(contact)
        return contact

    async def update_contact(
        self, contact_id: int, body: ContactModel, user: User
    ) -> Contact | None:
        """
        Update a Contact with the given attributes.

        Args:
            contact_id: The id of the Contact to update.
            body: A ContactModel with the attributes to assign to the Contact.
            user: The User who owns the Contact.

        Returns:
            The updated Contact, or None if no Contact with the given id exists.
        """
        contact = await self.get_contact_by_id(contact_id, user)
        if contact:
            for key, value in body.dict(exclude_unset=True).items():
                setattr(contact, key, value)
            await self.db.commit()
            await self.db.refresh(contact)
        return contact

    async def remove_contact(self, contact_id: int, user: User) -> Contact | None:
        """
        Delete a Contact by its id.

        Args:
            contact_id: The id of the Contact to delete.
            user: The owner of the Contact to delete.

        Returns:
            The deleted Contact, or None if no Contact with the given id exists.
        """
        contact = await self.get_contact_by_id(contact_id, user)
        if contact:
            await self.db.delete(contact)
            await self.db.commit()
        return contact

    async def is_contact_exists(
        self, email: str, phone_number: str, user: User
    ) -> bool:
        """
        Check if a Contact with the given email or phone number exists.

        Args:
            email: The email of the Contact to check.
            phone_number: The phone number of the Contact to check.
            user: The owner of the Contact to check.

        Returns:
            True if the Contact exists, False otherwise.
        """
        query = (
            select(Contact)
            .filter_by(user=user)
            .where((Contact.email == email) | (Contact.phone_number == phone_number))
        )
        result = await self.db.execute(query)
        return result.scalars().first() is not None

    async def get_upcoming_birthdays(self, days: int, user: User) -> list[Contact]:
        """
        Get a list of Contacts with upcoming birthdays.

        Args:
            days: The number of days in the future to check.
            user: The owner of the Contacts to check.

        Returns:
            A list of Contacts with upcoming birthdays.
        """
        today = date.today()
        end_date = today + timedelta(days=days)

        query = (
            select(Contact)
            .filter_by(user=user)
            .where(
                or_(
                    func.date_part("day", Contact.birth_date).between(
                        func.date_part("day", today), func.date_part("day", end_date)
                    ),
                    and_(
                        func.date_part("day", end_date) < func.date_part("day", today),
                        or_(
                            func.date_part("day", Contact.birth_date)
                            >= func.date_part("day", today),
                            func.date_part("day", Contact.birth_date)
                            <= func.date_part("day", end_date),
                        ),
                    ),
                )
            )
            .order_by(func.date_part("day", Contact.birth_date).asc())
        )

        result = await self.db.execute(query)
        return result.scalars().all()
