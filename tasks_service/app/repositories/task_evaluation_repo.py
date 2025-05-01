from datetime import datetime

from sqlalchemy import and_, exists, func, select

from app.models.task_evaluation import TaskEvaluation
from app.repositories.base_repository import BaseRepository


class TaskEvaluationRepository(BaseRepository):
    """Репозиторий для оценок задач"""

    model: type[TaskEvaluation] = TaskEvaluation

    async def get_evaluations(self, employee_id: int) -> list[TaskEvaluation]:
        """Получение записей оценок работников"""
        stmt = select(self.model).where(self.model.employee_id == employee_id)
        return (await self.session.scalars(stmt)).all()

    async def get_average_quarterly_score(self, employee_id: int, start_date: datetime, end_date: datetime) -> float:
        """Возвращает среднее значение средней оценки работника за определенный период"""
        stmt = select(func.coalesce(func.avg(TaskEvaluation.average_score), 0.0)).where(
            and_(
                TaskEvaluation.employee_id == employee_id,
                TaskEvaluation.created_at >= start_date,
                TaskEvaluation.created_at < end_date,
            )
        )

        return (await self.session.execute(stmt)).scalar()

    async def get_average_department_score(self, employee_ids: list[int]) -> float:
        """Возвращает среднее значение средней оценки нескольких работников"""
        stmt = select(func.coalesce(func.avg(TaskEvaluation.average_score), 0.0)).where(
            and_(TaskEvaluation.employee_id.in_(employee_ids))
        )
        result = (await self.session.execute(stmt)).scalar()
        return result

    async def exists_by_task_id(self, task_id: int) -> bool:
        stmt = select(exists().where(self.model.task_id == task_id))
        return bool(await self.session.scalar(stmt))
