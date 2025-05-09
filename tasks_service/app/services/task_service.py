from app.models.tasks import Task
from app.services.base_task_service import BaseTaskService
from app.services.event_mixin import EventMixin


class TaskService(BaseTaskService, EventMixin):
    """Сервис для управления задачами с отправкой событий при добавлении и удалении задач в Calendar Service"""

    def __init__(self, /, session, rmq_producer):
        super().__init__(session=session, rmq_producer=rmq_producer)

    async def create_task(self, user, task_data) -> Task:
        """Создание задачи с добавление события в Calendar Service"""
        task = await super().create_task(user, task_data)
        await self.create_event(task)
        return task

    async def delete_task(self, user, task_id) -> None:
        """Удаление задачи с удалением события из Calendar Service"""
        deleted_task = await super().delete_task(user, task_id)
        await self.delete_event(deleted_task)

    async def update_task(self, task_id, update_data) -> Task:
        """Обновление задачи с обновлением события в Calendar Service"""
        updated_task = await super().update_task(task_id, update_data)
        await self.update_event(updated_task)
        return updated_task
