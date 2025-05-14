from datetime import datetime

from sqlalchemy import delete, exists, select, update

from app.logging_config import logger
from app.models.events import Event
from app.repositories.base_repository import BaseRepository


class EventRepository(BaseRepository):
    """Репозиторий управления событиями"""

    model: type[Event] = Event

    async def get_by_period(self, employee_id: int, start_time: datetime, end_time: datetime) -> list[Event]:
        """Получение событий за определенный период"""
        stmt = select(self.model).where(
            self.model.employee_id == employee_id,
            self.model.start_time < end_time,
            self.model.end_time > start_time,
        )
        return (await self.session.scalars(stmt)).all()

    async def delete_by_source(self, source_id: int, event_type: str, employee_id: int) -> None:
        """Удаление события по source_id, event_type, employee_id"""
        logger.info(
            f"Удаление события с идентификатором источника={source_id}, "
            f"типом события={event_type}, идентификатором сотрудника={employee_id}"
        )
        stmt = delete(self.model).where(
            self.model.source_id == source_id,
            self.model.event_type == event_type,
            self.model.employee_id == employee_id,
        )
        result = await self.session.execute(stmt)
        await self.session.commit()
        logger.info(f"Успешно удаленно {result.rowcount} записи из {self.model.__name__}")

    async def update_by_source(self, source_id: int, event_type: str, employee_id: int, **update_data) -> None:
        """Обновление события по source_id, event_type, employee_id"""
        logger.info(
            f"Удаление события с идентификатором источника={source_id}, "
            f"типом события={event_type}, идентификатором сотрудника={employee_id}"
        )
        stmt = (
            update(self.model)
            .where(
                self.model.source_id == source_id,
                self.model.event_type == event_type,
                self.model.employee_id == employee_id,
            )
            .values(**update_data)
        )
        result = await self.session.execute(stmt)
        await self.session.commit()
        logger.info(f"Успешно удаленно {result.rowcount} записи из {self.model.__name__}")

    async def has_events_in_period(self, employee_id: int, start_time: datetime, end_time: datetime) -> bool:
        """Запрос выполняет проверку на существования события за определенный период"""
        stmt = select(
            exists().where(
                self.model.employee_id == employee_id,
                self.model.start_time < end_time,
                self.model.end_time > start_time,
            )
        )
        return bool(await self.session.scalar(stmt))
