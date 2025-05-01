from sqlalchemy import select

from app.models.tasks import Task
from app.repositories.base_repository import BaseRepository


class TaskRepository(BaseRepository):
    """Репозиторий для пользователей"""

    model: type[Task] = Task

    async def get_tasks_by_assignee_id(self, assignee_id: int) -> list[Task]:
        stmt = select(self.model).where(self.model.assignee_id == assignee_id)
        return (await self.session.scalars(stmt)).all()

    async def get_tasks_by_team_id(self, team_id: int) -> list[Task]:
        stmt = select(self.model).where(self.model.team_id == team_id)
        return (await self.session.scalars(stmt)).all()
