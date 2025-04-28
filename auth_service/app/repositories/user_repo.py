from datetime import datetime, timezone

from sqlalchemy import select, update

from app.models.users import User
from app.repositories.base_repository import BaseRepository


class UserRepository(BaseRepository):
    """Репозиторий для пользователей"""

    model: type[User] = User

    async def get_user_by_email(self, email: str) -> User | None:
        """Получение пользователя по полю email"""
        result = await self.session.scalars(select(self.model).where(self.model.email == email))
        return result.first()

    async def soft_delete(self, id: int) -> None:
        """Удаление пользователя с возможностью восстановления"""
        stmt = (
            update(self.model)
            .where(self.model.id == id)
            .values(is_active=False, deleted_at=datetime.now(timezone.utc))
        )
        await self.session.execute(stmt)
        self.session.commit()

    async def restore(self, id: int) -> None:
        """Восстановление пользователя"""
        stmt = update(self.model).where(self.model.id == id).values(is_active=True, deleted_at=None)
        await self.session.execute(stmt)
        self.session.commit()
