from fastapi import HTTPException, status
from sqlalchemy.exc import SQLAlchemyError
from sqlalchemy.ext.asyncio import AsyncSession

from app.clients.calendar_service_client import CalendarServiceClient
from app.clients.team_client import TeamServiceClient
from app.models.tasks import Task, TaskStatus
from app.repositories.task_repo import TaskRepository
from app.schemas.event_webhooks import NewEventHook
from app.schemas.tasks import TaskCreate, TaskUpdate
from app.schemas.users import User


class TaskService:
    """Сервис для управления задачами"""

    def __init__(self, session: AsyncSession):
        self.session = session
        self.repo = TaskRepository(session)
        self.team_client = TeamServiceClient()
        self.calendar_client = CalendarServiceClient()

    async def _get_task_or_404(self, task_id: int) -> Task:
        task = await self.repo.get(task_id)
        if not task:
            raise HTTPException(status_code=404, detail="Задача не найдена")
        return task

    async def get_tasks(self, team_id: int) -> list[Task]:
        """Получение задач команды"""
        return await self.repo.get_tasks_by_team_id(team_id)

    async def get_task(self, task_id: int) -> Task:
        """Получение задачи по идентификатору"""
        task = await self._get_task_or_404(task_id)
        return task

    async def create_task(self, user: User, task_data: TaskCreate) -> Task:
        """Создание задачи"""
        # Проверяем принадлежность исполнителя к команде
        assignee_membership = await self.team_client.get_employee(task_data.team_id, task_data.assignee_id)
        if not assignee_membership:
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST, detail="Исполнитель не является членом команды"
            )
        try:
            task = await self.repo.create(**task_data.model_dump(exclude_unset=True), creator_id=user.id)
            await self.create_event(task, user.id)
            return task
        except SQLAlchemyError as e:
            HTTPException(status_code=500, detail=str(e))

    async def update_task(self, task_id: int, update_data: TaskUpdate) -> Task:
        """Обновление задачи"""
        task = await self._get_task_or_404(task_id)
        if update_data.assignee_id:
            membership = await self.team_client.get_employee(task.team_id, update_data.assignee_id)
            if not membership:
                raise HTTPException(status_code=400, detail="Новый исполнитель не является членом команды")

        updated_task = await self.repo.update(task_id, **update_data.model_dump(exclude_unset=True))
        return updated_task

    async def delete_task(self, user: User, task_id: int) -> None:
        """Удаление завершенной задачи"""
        task = await self._get_task_or_404(task_id)
        # Удаляем только завершённые
        if task.status != TaskStatus.COMPLETED:
            raise HTTPException(status_code=400, detail="Задача еще не завершена")
        await self.delete_event(task, user.id)
        await self.repo.delete(task_id)

    async def get_assigned_tasks(self, user: User) -> list[Task]:
        """Получение поставленных задач"""
        tasks = await self.repo.get_tasks_by_assignee_id(user.id)
        return tasks

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
