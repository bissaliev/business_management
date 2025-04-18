from app.clients.calendar_service_client import CalendarServiceClient
from app.models.tasks import Task
from app.schemas.event_webhooks import NewEventHook


class EventMixin:
    """Класс миксин добавляет методы для управления событиями в Calendar Service"""

    calendar_client = CalendarServiceClient()

    async def create_event(self, task: Task, user_id: int):
        """Создание события в Calendar Service"""
        event_data = NewEventHook.model_validate(task, by_alias=True).model_dump(mode="json", exclude=["employee_id"])
        event_data["employee_id"] = user_id
        await self.calendar_client.send_meeting_webhook(event_data)

    async def verify_event(self, task: Task, user_id: int) -> bool:
        """Проверка на существование события в Calendar Service"""
        event_data = NewEventHook.model_validate(task, by_alias=True).model_dump(
            mode="json", include=["start_time", "end_time"]
        )
        event_data["employee_id"] = user_id
        return await self.calendar_client.verify_event_webhook(event_data)

    async def delete_event(self, task: Task, user_id: int):
        """Удаление события из Calendar Service"""
        event_data = NewEventHook.model_validate(task, by_alias=True).model_dump(
            mode="json", include=["source_id", "event_type"]
        )
        event_data["employee_id"] = user_id
        await self.calendar_client.delete_meeting_webhook(event_data)
