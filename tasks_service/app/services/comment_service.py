from fastapi import HTTPException, status
from sqlalchemy.ext.asyncio import AsyncSession

from app.models.comments import Comment
from app.repositories.comment_repo import CommentRepository
from app.repositories.task_repo import TaskRepository
from app.schemas.users import User


class CommentService:
    """Сервис для управления комментариями"""

    def __init__(self, session: AsyncSession):
        self.session = session
        self.repo = CommentRepository(session)
        self.task_repo = TaskRepository(session)

    async def create_comment(self, task_id: int, user: User, comment_data: dict) -> Comment:
        """Создание комментариев"""
        task = await self.task_repo.get(task_id)
        if not task:
            raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Задача не найдена")
        comment_data["task_id"] = task.id
        comment_data["user_id"] = user.id
        comment = await self.repo.create(**comment_data)
        return comment

    async def update_comment(self, task_id: int, comment_id: int, user: User, comment_data: dict) -> Comment:
        """Обновление комментариев"""
        task = await self.task_repo.get(task_id)
        if not task:
            raise HTTPException(status_code=404, detail="Задача не найдена")
        comment = await self.repo.get(comment_id)
        if not comment:
            raise HTTPException(status_code=404, detail="Комментарий не найден")
        if comment.user_id != user.id:
            raise HTTPException(status_code=403, detail="Нет прав на изменение комментария")
        return await self.repo.update(comment_id, **comment_data)

    async def get_comments_by_task_id(self, task_id: int) -> list[Comment]:
        """Получение всех комментариев задачи"""
        task = await self.task_repo.get(task_id)
        if not task:
            raise HTTPException(status_code=404, detail="Задача не найдена")
        return await self.repo.get_by_task_id(task_id)

    async def delete_comment(self, task_id: int, user: User, comment_id: int) -> None:
        """Удаление комментария пользователем"""
        task = await self.task_repo.get(task_id)
        if not task:
            raise HTTPException(status_code=404, detail="Задача не найдена")
        comment = await self.repo.get(comment_id)
        if not comment:
            raise HTTPException(status_code=404, detail="Комментарий не найден")
        if comment.user_id != user.id:
            raise HTTPException(status_code=403, detail="Нет прав на изменение комментария")
        await self.repo.delete(comment_id)
