from fastapi import HTTPException
from sqlalchemy.ext.asyncio import AsyncSession

from app.auth import get_password_hash
from app.models.users import User
from app.repositories.user_repo import UserRepository


class UserService:
    """Сервис для управления пользователями"""

    def __init__(self, session: AsyncSession):
        self.session = session
        self.repo = UserRepository(session)

    async def get_users(self) -> list[User]:
        """Получение всех пользователей"""
        return await self.repo.get_all()

    async def create(self, user_data: dict):
        """Создание пользователя"""
        if await self.repo.get_user_by_email(user_data["email"]):
            raise HTTPException(status_code=409, detail="Пользователь с таким email существует")

        password = user_data.pop("password")
        hashed_password = get_password_hash(password)
        user_data["hashed_password"] = hashed_password
        return await self.repo.create(user_data)

    async def get_user(self, id: int) -> User:
        """Получение одного пользователя"""
        user = await self.repo.get(id)
        if not user:
            raise HTTPException(status_code=404, detail="Пользователь не найден")
        return user

    async def update(self, id: int, user_data: dict) -> User:
        """Обновление данных пользователя"""
        if not await self.repo.exists(id):
            raise HTTPException(status_code=404, detail="Пользователь не найден")
        return await self.repo.update(id, user_data)

    async def soft_delete_user(self, id: int) -> None:
        """Удаление пользователя с возможностью восстановления"""
        if not await self.repo.exists(id):
            raise HTTPException(status_code=404, detail="Пользователь не найден")
        await self.repo.soft_delete(id)

    async def restore_user(self, id: int) -> None:
        """Восстановление пользователя"""
        if not await self.repo.exists(id):
            raise HTTPException(status_code=404, detail="Пользователь не найден")
        await self.repo.restore(id)
