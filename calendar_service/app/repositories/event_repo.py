from datetime import datetime

from sqlalchemy import delete, exists, select

from app.models.events import Event
from app.repositories.base_repository import BaseRepository


class EventRepository(BaseRepository):
    """Репозиторий управления событиями"""

    model = Event

    async def get_by_period(self, employee_id: int, start_time: datetime, end_time: datetime) -> list[Event]:
        """Получение событий за определенный период"""
        stmt = select(self.model).where(
            self.model.employee_id == employee_id,
            self.model.start_time >= start_time,
            self.model.start_time < end_time,
        )
        return (await self.session.scalars(stmt)).all()

    async def delete_by_source(self, source_id: int, event_type: str, employee_id: int) -> None:
        """Удаление события по source_id, event_type, employee_id"""
        stmt = delete(self.model).where(
            self.model.source_id == source_id,
            self.model.event_type == event_type,
            self.model.employee_id == employee_id,
        )
        await self.session.execute(stmt)
        await self.session.commit()

    async def verify_event(self, employee_id: int, start_time: datetime, end_time: datetime) -> list[Event]:
        """Запрос выполняет проверку на существования события за определенный период"""
        stmt = select(
            exists(self.model).where(
                self.model.employee_id == employee_id,
                self.model.start_time >= start_time,
                self.model.start_time < end_time,
            )
        )
        return await self.session.scalar(stmt)
