from sqlalchemy import literal, select
from sqlalchemy.dialects.postgresql import JSONB

from app.models.meeting import Meeting
from app.repositories.base_repository import BaseRepository


class MeetingRepository(BaseRepository):
    """Репозиторий для пользователей"""

    model = Meeting

    async def list_meetings(self, employee_id: int, team_id: int | None = None) -> list[Meeting]:
        stmt = select(self.model)
        if team_id:
            stmt = stmt.where(self.model.team_id == team_id)
        else:
            stmt = stmt.where(
                Meeting.participants.contains(literal([employee_id], type_=JSONB))
                | (self.model.creator_id == employee_id)
            )
        meetings = (await self.session.execute(stmt)).scalars().all()
        return meetings
