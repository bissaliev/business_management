from fastapi import HTTPException, status
from sqlalchemy.ext.asyncio import AsyncSession

from app.repositories.event_repo import EventRepository
from app.schemas.event_webhooks import EventParams, NewEventHook


class EventWebhookService:
    """Сервис для управления событиями в вебхуках"""

    def __init__(self, session: AsyncSession):
        self.repo = EventRepository(session)

    async def create_event(self, event_data: NewEventHook) -> None:
        """Создание события"""
        await self.repo.create(**event_data.model_dump())

    async def delete_event(self, event_data: EventParams) -> None:
        """Удаление события"""
        await self.repo.delete_by_source(**event_data.model_dump())

    async def has_events_in_period(self, event_data: EventParams) -> None:
        """Проверка на существование события в определенный период"""
        event = await self.repo.has_events_in_period(**event_data.model_dump())
        if not event:
            raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Not found event")
