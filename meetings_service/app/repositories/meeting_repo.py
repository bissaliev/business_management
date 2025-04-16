from sqlalchemy import and_, or_, select, update
from sqlalchemy.orm import selectinload

from app.models.meeting import Meeting, MeetingParticipant
from app.repositories.base_repository import BaseRepository


class MeetingRepository(BaseRepository):
    """Репозиторий для встреч"""

    model = Meeting

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

    async def get_meeting(self, employee_id: int, meeting_id: int) -> Meeting:
        """Получение объект встреч по id команды и идентификатору работника"""
        stmt = (
            select(self.model)
            .outerjoin(MeetingParticipant, self.model.id == MeetingParticipant.meeting_id)
            .options(selectinload(self.model.participants))
            .where(
                and_(
                    self.model.id == meeting_id,
                    or_(self.model.creator_id == employee_id, MeetingParticipant.participant_id == employee_id),
                )
            )
        )
        meeting = (await self.session.execute(stmt)).scalars().first()
        return meeting

    async def update_meeting(self, meeting_id: int, **update_data: dict) -> Meeting:
        """Обновление встречи"""
        stmt = update(self.model).where(self.model.id == meeting_id).values(**update_data).returning(self.model)
        return (await self.session.scalars(stmt)).first()
