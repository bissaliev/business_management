from fastapi import HTTPException, status
from sqlalchemy.ext.asyncio import AsyncSession

from app.models.events import Event
from app.repositories.event_repo import EventRepository
from app.schemas.events import EventCreate, EventUpdate
from app.schemas.users import User


class EventService:
    """Сервис для управления событиями"""

    def __init__(self, session: AsyncSession):
        self.repo = EventRepository(session)

    async def create_event(self, event_data: EventCreate, user: User) -> Event:
        """Создание события"""
        return await self.repo.create(employee_id=user.id, **event_data.model_dump(exclude_unset=True))

    async def update_event(self, event_id: int, event_data: EventUpdate, user: User) -> Event:
        """Обновление событий"""
        event = await self.repo.get(event_id)
        if not (event and event.employee_id == user.id):
            raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail="Событие не найдено")
        return await self.repo.update(event_id, **event_data.model_dump(exclude_unset=True))

    async def get_event(self, event_id: int, user: User) -> None:
        """Получение события"""
        event = await self.repo.get(event_id)
        if not (event and event.employee_id == user.id):
            raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail="Событие не найдено")
        return event

    async def delete_event(self, event_id: int, user: User) -> None:
        """Удаление события"""
        event = await self.repo.get(event_id)
        if not (event and event.employee_id == user.id):
            raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail="Событие не найдено")
        await self.repo.delete(event_id)
