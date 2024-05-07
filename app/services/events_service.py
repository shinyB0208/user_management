from builtins import Exception, bool, classmethod, int, str
from datetime import datetime
from typing import Optional, Tuple, List,Dict
from pydantic import ValidationError
from sqlalchemy import func, update, select, delete
from sqlalchemy.exc import SQLAlchemyError
from sqlalchemy.ext.asyncio import AsyncSession
from app.models.models import Event
from app.schemas.events_schema import EventCreate, EventUpdate
import logging
from uuid import UUID

logger = logging.getLogger(__name__)

class EventService:
    @classmethod
    async def _execute_query(cls, session: AsyncSession, query):
        try:
            result = await session.execute(query)
            await session.commit()
            return result
        except SQLAlchemyError as e:
            logger.error(f"Database error: {e}")
            await session.rollback()
            return None

    @classmethod
    async def get_all_events(cls, session: AsyncSession, page: int, page_size: int) -> Tuple[List[Event], int]:
        query = select(Event).offset(page).limit(page_size)
        result = await cls._execute_query(session, query)
        return result.scalars().all() if result else []

    @classmethod
    async def get_by_id(cls, session: AsyncSession, event_id: UUID) -> Optional[Event]:
        query = select(Event).filter_by(id=event_id)
        result = await cls._execute_query(session, query)
        return result.scalar() if result else None

    @classmethod
    async def create(cls, session: AsyncSession, event_data: Dict[str, str], user_id: str) -> Optional[Event]:
        try:
            validated_data = EventCreate(**event_data).model_dump()
            validated_data["created_by"] = user_id
            new_event = Event(**validated_data)
            new_event.created_by =  user_id
            session.add(new_event)
            await session.commit()
            return new_event
        except ValidationError as e:
            logger.error(f"Validation error during event creation: {e}")
            await session.rollback()
            return None

    @classmethod
    async def update(cls, session: AsyncSession, event_id: UUID, event_data: Dict[str, str]) -> Optional[Event]:
        try:
            data = EventUpdate(**event_data).model_dump(exclude_unset=True)
            event = await cls.get_by_id(session, event_id)
            if not event:
                return None
            query = update(Event).where(Event.id == event_id).values(**data)
            await cls._execute_query(session, query)
            
            updated_event = await cls.get_by_id(session, event_id)
            session.refresh(updated_event)  # Explicitly refresh the updated user object
            logger.info(f"Event {event_id} updated successfully.")
            return updated_event
        except ValidationError as e:
            logger.error(f"Validation error during event update: {e}")
            await session.rollback()
            return None

    @classmethod
    async def delete(cls, session: AsyncSession, event_id: str) -> bool:
        event = await cls.get_by_id(session, event_id)
        if not event:
            return False

        query = delete(Event).where(Event.id == event_id)
        result = await cls._execute_query(session, query)
        return result is not None
    
    @classmethod
    async def count(cls, session: AsyncSession) -> int:
        """
        Count the number of users in the database.

        :param session: The AsyncSession instance for database access.
        :return: The count of users.
        """
        query = select(func.count()).select_from(Event)
        result = await session.execute(query)
        count = result.scalar()
        return count