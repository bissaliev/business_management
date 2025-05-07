from sqlalchemy import delete, exists, select

from app.models.meeting import MeetingParticipant
from app.repositories.base_repository import BaseRepository


class MeetingParticipantRepository(BaseRepository):
    """Репозиторий для управления участниками встреч"""

    model: type[MeetingParticipant] = MeetingParticipant

    async def exists_participant(self, meeting_id: int, participant_id: int) -> bool:
        """Проверка на существование участника во встрече"""
        stmt = select(exists().where(self.model.meeting_id == meeting_id, self.model.participant_id == participant_id))
        return bool(await self.session.scalar(stmt))

    async def delete_participant(self, meeting_id: int, participant_id: int) -> bool:
        """Удаление участника из встречи"""
        stmt = delete(self.model).where(
            self.model.meeting_id == meeting_id, self.model.participant_id == participant_id
        )
        result = await self.session.execute(stmt)
        return result.rowcount > 0

    async def get_participant_ids(self, meeting_id: int) -> list[int]:
        """Получение идентификаторов участников встречи"""
        stmt = select(self.model.participant_id).where(self.model.meeting_id == meeting_id)
        return (await self.session.scalars(stmt)).all()
