from app.services.base_task_service import BaseTaskService
from app.services.event_mixin import EventMixin


class TaskService(BaseTaskService, EventMixin):
    """Сервис для управления задачами с отправкой событий при добавлении и удалении задач в Calendar Service"""

    async def create_task(self, user, task_data):
        task = await super().create_task(user, task_data)
        await self.create_event(task, user.id)
        return task

    async def delete_task(self, user, task_id):
        deleted_task = await super().delete_task(user, task_id)
        await self.delete_event(deleted_task, user.id)
