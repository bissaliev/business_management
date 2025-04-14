from sqlalchemy import select

from app.models.comments import Comment
from app.repositories.base_repository import BaseRepository


class CommentRepository(BaseRepository):
    """Репозиторий для пользователей"""

    model = Comment

    async def get_by_task_id(self, task_id: int) -> list[Comment]:
        """Получение комментариев по идентификатору задачи"""
        stmt = select(self.model).where(self.model.task_id == task_id)
        return (await self.session.scalars(stmt)).all()
