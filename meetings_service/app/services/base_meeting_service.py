from fastapi import HTTPException, status
from sqlalchemy.ext.asyncio import AsyncSession

from app.logging_config import logger
from app.models.meeting import Meeting
from app.repositories.meeting_participant_repo import MeetingParticipantRepository
from app.repositories.meeting_repo import MeetingRepository
from app.schemas.meeting import MeetingCreate, MeetingUpdate, Participant
from app.schemas.users import User


class BaseMeetingService:
    """Базовый сервис для управления встречами"""

    def __init__(self, session: AsyncSession):
        self.session = session
        self.repo = MeetingRepository(session)
        self.meeting_participant_repo = MeetingParticipantRepository(session)

    async def _get_meeting_or_404(self, meeting_id: int, user_id: int) -> Meeting:
        meeting = await self.repo.get(meeting_id)
        if not meeting:
            raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Встреча не найдена")
        if meeting.creator_id != user_id:
            raise HTTPException(status_code=status.HTTP_403_FORBIDDEN, detail="Нет прав доступа")
        return meeting

    async def create_meeting(self, user: User, new_data: MeetingCreate) -> Meeting:
        """Создание встречи"""
        meeting = await self.repo.create(creator_id=user.id, **new_data.model_dump())
        self.session.commit()
        logger.info(f"Создание встречи с идентификатором {meeting.id=}")
        return meeting

    async def get_list_meetings(self, user: User, team_id: int | None = None) -> list[Meeting]:
        """Получение предстоящих встреч для текущего пользователя"""
        meetings = await self.repo.list_meetings(user.id, team_id)
        return meetings

    async def get_meeting(self, user: User, meeting_id: int) -> list[Meeting]:
        """Получение встречи пользователя"""
        return await self._get_meeting_or_404(meeting_id, user.id)

    async def update_meeting(self, user: User, meeting_id: int, update_data: MeetingUpdate) -> list[Meeting]:
        """Редактирование встречи"""
        await self._get_meeting_or_404(meeting_id, user.id)
        meeting: Meeting = await self.repo.update_meeting(meeting_id, **update_data.model_dump(exclude_unset=True))
        return meeting

    async def delete_meeting(self, user: User, meeting_id: int) -> Meeting:
        """Удаление встречи"""
        meeting = await self._get_meeting_or_404(meeting_id, user.id)
        await self.repo.delete(meeting_id)
        await self.session.commit()
        logger.info(f"Удаление встречи с идентификатором {meeting_id=}")
        return meeting

    async def add_participant(self, meeting_id: int, participant: Participant, user: User) -> Meeting:
        """Добавить участника ко встрече"""
        meeting = await self._get_meeting_or_404(meeting_id, user.id)
        if await self.meeting_participant_repo.exists_participant(meeting_id, participant.participant_id):
            raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail="Участник уже присоединен к встрече")
        await self.meeting_participant_repo.create(meeting_id=meeting_id, participant_id=participant.participant_id)
        await self.session.commit()
        logger.info(f"Добавление участника {participant.participant_id=} ко встрече с идентификатором {meeting_id=}")
        return meeting

    async def delete_participant(self, meeting_id: int, participant_id: int, user: User) -> Meeting:
        """Удаление участника из встречи"""
        meeting = await self._get_meeting_or_404(meeting_id, user.id)
        if not await self.meeting_participant_repo.exists_participant(meeting_id, participant_id):
            raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail="Участник не присоединен к встрече")
        await self.meeting_participant_repo.delete_participant(meeting_id=meeting_id, participant_id=participant_id)
        await self.session.commit()
        logger.info(f"Удаление участника {participant_id=} из встречи с идентификатором {meeting_id=}")
        return meeting
