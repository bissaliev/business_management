from fastapi import HTTPException, status
from sqladmin import ModelView

from app.clients.team_client import TeamServiceClient
from app.models.task_evaluation import TaskEvaluation
from app.models.tasks import Task
from app.services.event_mixin import EventMixin


class BaseTaskAdmin(ModelView, model=Task):
    """Базовое представление для модели Task"""

    team_client = TeamServiceClient()

    column_list = [Task.id, Task.title]
    form_excluded_columns = [Task.created_at, Task.updated_at, "task_evaluations"]

    async def on_model_change(self, data, model, is_created, request) -> None:
        assignee_membership = await self.team_client.get_employee(data["team_id"], data["assignee_id"])
        if not assignee_membership:
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST, detail="Исполнитель не является членом команды"
            )


class TaskAdmin(BaseTaskAdmin, EventMixin):
    """Представление модели Task с добавление отправки событий на сервис Calendar Service"""

    async def after_model_change(self, data, model, is_created, request):
        """Создаем событие в Calendar Service"""
        await self.create_event(model, model.creator_id)

    async def after_model_delete(self, model, request):
        """Удаляем событие в Calendar Service"""
        await self.delete_event(model, model.creator_id)


class TaskEvaluationAdmin(ModelView, model=TaskEvaluation):
    """Представление модели TaskEvaluation"""

    form_excluded_columns = [TaskEvaluation.created_at, TaskEvaluation.average_score]

    async def on_model_change(self, data, model, is_created, request) -> None:
        timeliness = data["timeliness"]
        quality = data["quality"]
        completeness = data["completeness"]

        if not (1 <= timeliness <= 5 and 1 <= quality <= 5 and 1 <= completeness <= 5):
            raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail="Оценка должна быть от 1 до 5")

        data["average_score"] = (data["timeliness"] + data["quality"] + data["completeness"]) / 3
