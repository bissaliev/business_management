from fastapi import HTTPException, status
from sqlalchemy.ext.asyncio import AsyncSession

from app.clients.team_client import TeamServiceClient
from app.logging_config import logger
from app.models.tasks import Task, TaskStatus
from app.repositories.task_repo import TaskRepository
from app.schemas.tasks import TaskCreate, TaskUpdate
from app.schemas.users import User


class BaseTaskService:
    """Базовый Сервис для управления задачами"""

    def __init__(self, /, session: AsyncSession, **kwargs):
        super().__init__(**kwargs)
        self.session = session
        self.repo = TaskRepository(session)
        self.team_client = TeamServiceClient()

    async def _get_task_or_404(self, task_id: int) -> Task:
        """Получение объекта Task или выброс исключения 404"""
        task = await self.repo.get(task_id)
        if not task:
            raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Задача не найдена")
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
        task = await self.repo.create(**task_data.model_dump(exclude_unset=True), creator_id=user.id)
        await self.session.commit()
        logger.info(f"Создание задачи {task.id=}")
        return task

    async def update_task(self, task_id: int, update_data: TaskUpdate) -> Task:
        """Обновление задачи"""
        task = await self._get_task_or_404(task_id)
        if update_data.assignee_id:
            membership = await self.team_client.get_employee(task.team_id, update_data.assignee_id)
            if not membership:
                raise HTTPException(
                    status_code=status.HTTP_400_BAD_REQUEST, detail="Новый исполнитель не является членом команды"
                )

        updated_task = await self.repo.update(task_id, **update_data.model_dump(exclude_unset=True))
        await self.session.commit()
        logger.info(f"Обновление задачи {task_id=}")
        return updated_task

    async def delete_task(self, user: User, task_id: int) -> None:
        """Удаление завершенной задачи"""
        task = await self._get_task_or_404(task_id)
        # Удаляем только завершённые
        if task.status != TaskStatus.COMPLETED:
            raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail="Задача еще не завершена")
        await self.repo.delete(task_id)
        await self.session.commit()
        logger.info(f"Удаление задачи {task.id=}")
        return task

    async def get_assigned_tasks(self, user: User) -> list[Task]:
        """Получение поставленных задач"""
        tasks = await self.repo.get_tasks_by_assignee_id(user.id)
        return tasks
