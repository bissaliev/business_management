from sqlalchemy import select, update
from sqlalchemy.orm import selectinload

from app.models.meeting import Meeting, MeetingParticipant
from app.repositories.base_repository import BaseRepository


class MeetingRepository(BaseRepository):
    """Репозиторий для встреч"""

    model: type[Meeting] = Meeting

    async def list_meetings(self, employee_id: int, team_id: int | None = None) -> list[Meeting]:
        """Получение списка встреч с фильтрацией по идентификатору команды и идентификатору работника"""
        stmt = (
            select(self.model)
            .outerjoin(MeetingParticipant, self.model.id == MeetingParticipant.meeting_id)
            .options(selectinload(self.model.participants))
        )
        if team_id:
            stmt = stmt.where(self.model.team_id == team_id)
        else:
            stmt = stmt.where(
                (self.model.creator_id == employee_id) | (MeetingParticipant.participant_id == employee_id)
            )
        meetings = (await self.session.execute(stmt)).scalars().all()
        return meetings

    async def update_meeting(self, meeting_id: int, **update_data: dict) -> Meeting:
        """Обновление встречи"""
        stmt = update(self.model).where(self.model.id == meeting_id).values(**update_data).returning(self.model)
        return (await self.session.scalars(stmt)).first()
