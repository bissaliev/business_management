from fastapi import HTTPException, status

from app.services.base_meeting_service import BaseMeetingService
from app.services.event_mixin import EventMixin


class MeetingService(BaseMeetingService, EventMixin):
    """Сервис для управления встречами"""

    async def create_meeting(self, user, new_data):
        """Создание встречи с добавлением создания события в Calendar Service"""
        meeting = await super().create_meeting(user, new_data)
        await self.create_event(meeting, user.id)
        return meeting

    async def delete_meeting(self, user, meeting_id):
        """Удаление встречи с добавлением удаления события из Calendar Service"""
        meeting = await super().delete_meeting(user, meeting_id)
        await self.delete_event(meeting, user.id)

    async def add_participant(self, meeting_id, participant, user):
        """
        Добавление участника ко встречи с созданием события для участника в Calendar Service
        и проверкой наличия события
        """
        meeting = await self.repo.get(meeting_id)
        if await self.has_events_in_period(meeting, participant.participant_id):
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST, detail="У пользователя назначено событие на это время"
            )
        await self.create_event(meeting, participant.participant_id)
        return await super().add_participant(meeting_id, participant, user)

    async def delete_participant(self, meeting_id, participant_id, user):
        """Удаление участника из встречи с удалением события из Calendar Service"""
        meeting = await super().delete_participant(meeting_id, participant_id, user)
        await self.delete_event(meeting, user.id)
