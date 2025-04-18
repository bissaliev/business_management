from fastapi import HTTPException, status
from sqlalchemy.ext.asyncio import AsyncSession

from app.models.comments import Comment
from app.repositories.comment_repo import CommentRepository
from app.repositories.task_repo import TaskRepository
from app.schemas.comments import CommentCreate
from app.schemas.users import User


class CommentService:
    """Сервис для управления комментариями"""

    def __init__(self, session: AsyncSession):
        self.session = session
        self.repo = CommentRepository(session)
        self.task_repo = TaskRepository(session)

    async def create_comment(self, task_id: int, user: User, comment_data: CommentCreate) -> Comment:
        """Создание комментариев"""
        task = await self._get_task_or_404(task_id)
        comment = await self.repo.create(task_id=task.id, user_id=user.id, **comment_data.model_dump())
        return comment

    async def update_comment(self, task_id: int, comment_id: int, user: User, comment_data: CommentCreate) -> Comment:
        """Обновление комментариев"""
        await self._get_task_or_404(task_id)
        await self._require_author(comment_id, user.id)
        return await self.repo.update(comment_id, **comment_data.model_dump(exclude_unset=True))

    async def get_comments_by_task_id(self, task_id: int) -> list[Comment]:
        """Получение всех комментариев задачи"""
        task = await self._get_task_or_404(task_id)
        return await self.repo.get_by_task_id(task.id)

    async def delete_comment(self, task_id: int, user: User, comment_id: int) -> None:
        """Удаление комментария пользователем"""
        await self._get_task_or_404(task_id)
        await self._require_author(comment_id, user.id)
        await self.repo.delete(comment_id)

    async def _get_task_or_404(self, task_id):
        """Получить объект Task или вызвать исключение HTTP_404_NOT_FOUND"""
        task = await self.task_repo.get(task_id)
        if not task:
            raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Задача не найдена")
        return task

    async def _get_comment_or_404(self, comment_id):
        """Получить объект Comment или вызвать исключение HTTP_404_NOT_FOUND"""
        comment = await self.repo.get(comment_id)
        if not comment:
            raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Комментарий не найден")
        return comment

    async def _require_author(self, comment_id: int, user_id: int):
        """Получить объект Comment если пользователь автор комментария"""
        comment = await self._get_comment_or_404(comment_id)
        if comment.user_id != user_id:
            raise HTTPException(status_code=status.HTTP_403_FORBIDDEN, detail="Нет прав на изменение комментария")
        return comment
