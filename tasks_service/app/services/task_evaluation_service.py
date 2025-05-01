from fastapi import HTTPException, status
from sqlalchemy.ext.asyncio import AsyncSession

from app.clients.org_client import OrgServiceClient
from app.logging_config import logger
from app.models.task_evaluation import TaskEvaluation
from app.models.tasks import Task, TaskStatus
from app.repositories.task_evaluation_repo import TaskEvaluationRepository
from app.repositories.task_repo import TaskRepository
from app.schemas.task_evaluation import EmployeeEvaluationSummary, TaskEvaluationCreate
from app.schemas.users import User
from app.utils.dates import get_last_quarter, get_quarter_dates


class TaskEvaluationService:
    """Сервис для управления оценками задач"""

    def __init__(self, session: AsyncSession):
        self.session = session
        self.repo = TaskEvaluationRepository(session)
        self.task_repo = TaskRepository(session)
        self.org_client = OrgServiceClient()

    async def create_evaluation(
        self, task_id: int, user: User, evaluation_data: TaskEvaluationCreate
    ) -> TaskEvaluation:
        """Создание записи оценки задачи"""
        # Проверяем задачу
        task = await self._get_completed_task_or_404(task_id)

        # Проверяем, что оценка ещё не выставлена
        if await self.repo.exists_by_task_id(task.id):
            raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail="Задача уже оценена")

        # Создаём среднюю оценку
        average_score = (evaluation_data.timeliness + evaluation_data.quality + evaluation_data.completeness) / 3
        evaluation = await self.repo.create(
            task_id=task.id,
            employee_id=task.assignee_id,
            evaluator_id=user.id,
            average_score=average_score,
            **evaluation_data.model_dump(),
        )
        await self.session.commit()
        logger.info(f"Менеджер {user.id} поставил оценку работнику {task.assignee_id}")
        return evaluation

    async def get_evaluations(self, user: User) -> EmployeeEvaluationSummary:
        """Получение матрицы оценок работника"""

        employees = await self.org_client.get_membership(user.id)
        employee_ids = [i["employee_id"] for i in employees]
        # Получаем среднюю оценку по департаменту
        average_department_score = await self.repo.get_average_department_score(employee_ids)

        # Получаем среднюю оценку текущего пользователя за квартал
        quarter, year = get_last_quarter()
        start_date, end_date = get_quarter_dates(quarter, year)
        average_quarterly_score = await self.repo.get_average_quarterly_score(user.id, start_date, end_date)

        # Получаем все оценки текущего пользователя
        evaluations = await self.repo.get_evaluations(user.id)

        return EmployeeEvaluationSummary(
            employee_id=user.id,
            average_quarterly_score=average_quarterly_score,
            average_department_score=average_department_score,
            evaluations=evaluations,
        )

    async def _get_completed_task_or_404(self, task_id: int) -> Task:
        """Получение выполненной задачи или возбуждение исключение с ошибкой 404"""
        task = await self.task_repo.get(task_id)
        if not (task and task.status == TaskStatus.COMPLETED):
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND, detail="Выполненная задачи {task_id} не найдена"
            )
        return task
