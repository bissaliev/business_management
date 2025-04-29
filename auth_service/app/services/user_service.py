from fastapi import HTTPException, status
from sqlalchemy.ext.asyncio import AsyncSession

from app.clients.team_client import TeamServiceClient
from app.models.users import User
from app.repositories.user_repo import UserRepository
from app.security import get_password_hash


class UserService:
    """Сервис для управления пользователями"""

    def __init__(self, session: AsyncSession):
        self.session = session
        self.repo = UserRepository(session)
        self.team_client = TeamServiceClient()

    async def create(self, user_data: dict) -> User:
        """Создание пользователя"""
        if await self.repo.exists_email(user_data["email"]):
            raise HTTPException(status_code=status.HTTP_409_CONFLICT, detail="Пользователь с таким email существует")
        password = user_data.pop("password")
        team_code = user_data.pop("team_code")
        user = await self.repo.create(hashed_password=get_password_hash(password), **user_data)
        try:
            team = await self.team_client.add_employee_to_team(user.id, str(team_code))
        except Exception as e:
            raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail=f"Invalid team_code: {str(e)}") from e
        return await self.repo.update(user.id, team_id=team["team_id"])

    async def get_users(self) -> list[User]:
        """Получение всех пользователей"""
        return await self.repo.get_all()

    async def get_user(self, id: int) -> User:
        """Получение одного пользователя"""
        user = await self.repo.get(id)
        if not user:
            raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Пользователь не найден")
        return user

    async def update(self, id: int, user_data: dict) -> User:
        """Обновление данных пользователя"""
        if not await self.repo.exists(id):
            raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Пользователь не найден")
        return await self.repo.update(id, **user_data)

    async def soft_delete_user(self, id: int) -> None:
        """Удаление пользователя с возможностью восстановления"""
        if not await self.repo.exists(id):
            raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Пользователь не найден")
        await self.repo.soft_delete(id)

    async def restore_user(self, id: int) -> None:
        """Восстановление пользователя"""
        user = await self.repo.get(id)
        if not user:
            raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Пользователь не найден")
        await self.repo.restore(user.id)
