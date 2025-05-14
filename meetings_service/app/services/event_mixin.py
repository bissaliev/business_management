from app.clients.calendar_service_client import CalendarServiceClient
from app.clients.rabbitmq.event_publisher import EventPublisher
from app.logging_config import logger
from app.models.meeting import Meeting
from app.schemas.event_webhooks import NewEventHook
from app.schemas.meeting_events import EventType, MeetingCreatedEvent, MeetingDeletedEvent


class EventMixin:
    """Класс миксин добавляет методы для управления событиями в Calendar Service"""

    rmq_producer: EventPublisher | None = None
    calendar_client = CalendarServiceClient()

    def add_producer(self, rmq_producer: EventPublisher) -> None:
        self.rmq_producer = rmq_producer

    async def create_event(self, meeting: Meeting) -> None:
        """Создание события в Calendar Service"""
        payload = MeetingCreatedEvent.model_validate(meeting, by_alias=True).model_dump(mode="json")
        event = {"type": EventType.CREATED.value, "payload": payload}
        await self.rmq_producer.publish(event)
        logger.info(f"Событие о создании встречи {meeting.id} отправлено в сервисе Calendar Service")

    async def delete_event(self, meeting: Meeting) -> None:
        """Удаление события из Calendar Service"""
        payload = MeetingDeletedEvent.model_validate(meeting, by_alias=True).model_dump(mode="json")
        event = {"type": EventType.DELETED.value, "payload": payload}
        await self.rmq_producer.publish(event)
        logger.info(f"Событие о удалении встречи {meeting.id} отправлено в сервисе Calendar Service")

    async def update_event(self, meeting: Meeting) -> None:
        """Обновление события в Calendar Service"""
        payload = MeetingCreatedEvent.model_validate(meeting, by_alias=True).model_dump(mode="json")
        event = {"type": EventType.UPDATED.value, "payload": payload}
        await self.rmq_producer.publish(event)
        logger.info(f"Событие об обновлении встречи {meeting.id} отправлено в сервисе Calendar Service")

    # TODO: Придумать как сделать проверку события через RabbitMQ
    async def has_events_in_period(self, meeting: Meeting, user_id: int) -> bool:
        """Проверка на существование события в Calendar Service"""
        event_data = NewEventHook.model_validate(meeting, by_alias=True).model_dump(
            mode="json", include=["start_time", "end_time"]
        )
        event_data["employee_id"] = user_id
        return await self.calendar_client.has_events_in_period(event_data)
