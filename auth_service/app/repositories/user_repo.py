from datetime import datetime

from sqlalchemy import select, update

from app.models.users import User
from app.repositories.base_repository import BaseRepository


class UserRepository(BaseRepository):
    """Репозиторий для пользователей"""

    model = User

    async def get_user_by_email(self, email: str) -> User:
        """Получение пользователя по полю email"""
        result = await self.session.scalars(select(self.model).where(self.model.email == email))
        return result.first()

    async def soft_delete(self, id: int) -> User | None:
        """Удаление пользователя с возможностью восстановления"""
        stmt = update(self.model).where(self.model.id == id).values(is_active=False, deleted_at=datetime.now())
        result = await self.session.scalars(stmt)
        return result.first()

    async def restore(self, id: int) -> User | None:
        """Восстановление пользователя"""
        stmt = update(self.model).where(self.model.id == id).values(is_active=True, deleted_at=None)
        result = await self.session.scalars(stmt)
        return result.first()
