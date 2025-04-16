from fastapi import HTTPException, status
from sqlalchemy.ext.asyncio import AsyncSession

from app.clients.team_client import TeamServiceClient
from app.models.meeting import Meeting
from app.repositories.meeting_participant_repo import MeetingParticipantRepository
from app.repositories.meeting_repo import MeetingRepository
from app.schemas.meeting import MeetingCreate, MeetingUpdate, Participant
from app.schemas.users import User


class MeetingService:
    """Сервис для управления встречами"""

    def __init__(self, session: AsyncSession):
        self.session = session
        self.repo = MeetingRepository(session)
        self.meeting_participant_repo = MeetingParticipantRepository(session)
        self.team_client = TeamServiceClient()

    async def create_meeting(self, user: User, new_data: MeetingCreate) -> Meeting:
        """Создание встречи"""
        meeting = await self.repo.create(creator_id=user.id, **new_data.model_dump())
        return meeting

    async def get_list_meetings(self, user: User, team_id: int | None = None) -> list[Meeting]:
        """Получение предстоящих встреч для текущего пользователя"""
        meetings = await self.repo.list_meetings(user.id, team_id)
        return meetings

    async def get_meeting(self, user: User, meeting_id: int) -> list[Meeting]:
        meeting = await self.repo.get_meeting(user.id, meeting_id)
        if not meeting:
            raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Встреча не найдена")
        return meeting

    async def update_meeting(self, user: User, meeting_id: int, update_data: MeetingUpdate) -> list[Meeting]:
        """Редактирование встречи"""
        meeting = await self.repo.get(meeting_id)
        if not meeting:
            raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Встреча не найдена")
        if meeting.creator_id != user.id:
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST, detail="Редактирование встречи доступно только создателю"
            )
        meeting: Meeting = await self.repo.update_meeting(meeting_id, **update_data.model_dump(exclude_unset=True))
        return meeting

    async def delete_meeting(self, user: User, meeting_id: int) -> None:
        """Удаление встречи"""
        meeting = await self.repo.get(meeting_id)
        if not meeting:
            raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Встреча не найдена")
        if meeting.creator_id != user.id:
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST, detail="Редактирование встречи доступно только создателю"
            )
        await self.repo.delete(meeting_id)

    async def add_participant(self, meeting_id: int, participant: Participant, user: User):
        """Добавить участника ко встрече"""
        meeting = await self.repo.get(meeting_id)
        if not meeting:
            raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Встреча не найдена")
        if meeting.creator_id != user.id:
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail="Добавление участника встречи доступно только создателю",
            )
        if await self.meeting_participant_repo.exists_participant(meeting_id, participant.participant_id):
            raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail="Участника уже присоединен к встрече")
        await self.meeting_participant_repo.create(meeting_id=meeting_id, participant_id=participant.participant_id)

    async def delete_participant(self, meeting_id: int, participant_id: int, user: User):
        """Удаление участника из встречи"""
        meeting = await self.repo.get(meeting_id)
        if not meeting:
            raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Встреча не найдена")
        if meeting.creator_id != user.id:
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail="Удаление участника встречи доступно только создателю",
            )
        if not await self.meeting_participant_repo.exists_participant(meeting_id, participant_id):
            raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail="Участника не присоединен к встрече")
        await self.meeting_participant_repo.delete_participant(meeting_id=meeting_id, participant_id=participant_id)
