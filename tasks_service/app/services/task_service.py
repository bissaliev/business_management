from fastapi import HTTPException, status
from sqlalchemy.exc import SQLAlchemyError
from sqlalchemy.ext.asyncio import AsyncSession

from app.clients.team_client import TeamServiceClient
from app.models.tasks import Task, TaskStatus
from app.repositories.task_repo import TaskRepository
from app.schemas.users import User


class TaskService:
    """Сервис для управления задачами"""

    def __init__(self, session: AsyncSession):
        self.session = session
        self.repo = TaskRepository(session)
        self.team_client = TeamServiceClient()

    async def get_tasks(self, team_id: int) -> list[Task]:
        return await self.repo.get_tasks_by_team_id(team_id)

    async def get_task(self, task_id: int) -> Task:
        """Получение задачи"""
        task = await self.repo.get(task_id)
        if not task:
            raise HTTPException(status_code=404, detail="Задача не найдена")
        return task

    async def create_task(self, user: User, task_data: dict) -> Task:
        """Создание задачи"""
        assignee_membership = await self.team_client.get_employee(task_data["team_id"], task_data["assignee_id"])
        if not assignee_membership:
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST, detail="Исполнитель не является членом команды"
            )
        task_data |= {"creator_id": user.id}
        try:
            task = await self.repo.create(**task_data)
            return task
        except SQLAlchemyError as e:
            HTTPException(status_code=500, detail=str(e))

    async def update_task(self, task_id: int, update_data: dict) -> Task:
        """Обновление задачи"""
        task = await self.repo.get(task_id)
        if not task:
            raise HTTPException(status_code=404, detail="Задача не найдена")
        if "assignee_id" in update_data:
            membership = await self.team_client.get_employee(task.team_id, update_data["assignee_id"])
            if not membership:
                raise HTTPException(status_code=400, detail="Новый исполнитель не является членом команды")

        updated_task = await self.repo.update(task_id, **update_data)
        return updated_task

    async def delete_task(self, task_id: int) -> None:
        """Удаление завершенной задачи"""
        task = await self.repo.get(task_id)
        if not task:
            raise HTTPException(status_code=404, detail="Задача не найдена")
        # Удаляем только завершённые
        if task.status != TaskStatus.COMPLETED:
            raise HTTPException(status_code=400, detail="Задача еще не завершена")
        await self.repo.delete(task_id)

    async def get_assigned_tasks(self, user: User) -> list[Task]:
        """Получение поставленных задач"""
        tasks = await self.repo.get_tasks_by_assignee_id(user.id)
        return tasks
