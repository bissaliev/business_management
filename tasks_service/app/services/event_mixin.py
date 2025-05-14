from app.clients.rabbitmq.event_publisher import EventPublisher
from app.logging_config import logger
from app.models.tasks import Task
from app.schemas.task_events import EventType, TaskCreatedEvent, TaskDeletedEvent


class EventMixin:
    """Класс миксин добавляет методы для управления событиями в Calendar Service"""

    def __init__(self, /, rmq_producer: EventPublisher, **kwargs):
        super().__init__(**kwargs)
        self.rmq_producer = rmq_producer

    async def create_event(self, task: Task) -> None:
        """Создание события в Calendar Service"""
        payload = TaskCreatedEvent.model_validate(task, by_alias=True).model_dump(mode="json")
        event = {"type": EventType.CREATED.value, "payload": payload}
        await self.rmq_producer.publish(event)
        logger.info(f"Событие о создании задачи {task.id} отправлено в сервисе Calendar Service")

    async def delete_event(self, task: Task) -> None:
        """Удаление события из Calendar Service"""
        payload = TaskDeletedEvent.model_validate(task, by_alias=True).model_dump(mode="json")
        event = {"type": EventType.DELETED.value, "payload": payload}
        await self.rmq_producer.publish(event)
        logger.info(f"Событие о удалении задачи {task.id} отправлено в сервисе Calendar Service")

    async def update_event(self, task: Task) -> None:
        """Обновление события в Calendar Service"""
        payload = TaskCreatedEvent.model_validate(task, by_alias=True).model_dump(mode="json")
        event = {"type": EventType.UPDATED.value, "payload": payload}
        await self.rmq_producer.publish(event)
        logger.info(f"Событие об обновлении задачи {task.id} отправлено в сервисе Calendar Service")
