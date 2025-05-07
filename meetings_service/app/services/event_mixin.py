from app.clients.calendar_service_client import CalendarServiceClient
from app.logging_config import logger
from app.models.meeting import Meeting
from app.schemas.event_webhooks import NewEventHook


class EventMixin:
    """Класс миксин добавляет методы для управления событиями в Calendar Service"""

    calendar_client = CalendarServiceClient()

    async def create_event(self, meeting: Meeting, user_id: int):
        """Создание события в Calendar Service"""
        event_data = NewEventHook.model_validate(meeting, by_alias=True).model_dump(
            mode="json", exclude=["employee_id"]
        )
        event_data["employee_id"] = user_id
        await self.calendar_client.send_meeting_webhook(event_data)
        logger.info(f"Создание события для встречи {meeting.id=} в Calendar Service")

    async def has_events_in_period(self, meeting: Meeting, user_id: int) -> bool:
        """Проверка на существование события в Calendar Service"""
        event_data = NewEventHook.model_validate(meeting, by_alias=True).model_dump(
            mode="json", include=["start_time", "end_time"]
        )
        event_data["employee_id"] = user_id
        return await self.calendar_client.has_events_in_period(event_data)

    async def delete_event(self, meeting: Meeting, user_id: int):
        """Удаление события из Calendar Service"""
        event_data = NewEventHook.model_validate(meeting, by_alias=True).model_dump(
            mode="json", include=["source_id", "event_type"]
        )
        event_data["employee_id"] = user_id
        await self.calendar_client.delete_meeting_webhook(event_data)
        logger.info(f"Удаление события для встречи {meeting.id=} в Calendar Service")
