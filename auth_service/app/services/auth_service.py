from fastapi import HTTPException, status
from sqlalchemy.ext.asyncio import AsyncSession

from app.clients.team_client import TeamServiceClient
from app.logging_config import logger
from app.models.users import Status
from app.repositories.user_repo import UserRepository
from app.schemas.users import Token
from app.security import create_access_token, decode_access_token, verify_password


class AuthService:
    """Сервис для управления пользователями"""

    def __init__(self, session: AsyncSession):
        self.session = session
        self.repo = UserRepository(session)
        self.team_client = TeamServiceClient()

    async def authenticate_user(self, email: str, password: str):
        """Аутентификация пользователя"""
        user = await self.repo.get_user_by_email(email)
        if not (user and verify_password(password, user.hashed_password)):
            raise HTTPException(
                status_code=status.HTTP_401_UNAUTHORIZED,
                detail="Incorrect email or password",
                headers={"WWW-Authenticate": "Bearer"},
            )
        return user

    async def login(self, email: str, password: str) -> Token:
        """Вход пользователя"""
        user = await self.authenticate_user(email, password)
        if not user.is_active:
            raise HTTPException(status_code=status.HTTP_403_FORBIDDEN, detail="Inactive user")
        data = {"sub": str(user.id), "email": user.email, "status": user.status.value}
        role = await self.team_client.get_employee_role(user.id, user.team_id)
        data |= role
        access_token = create_access_token(data=data)
        logger.info(f"Пользователь {user.email} успешно вошел в систему")
        return Token(access_token=access_token, token_type="bearer")

    async def get_current_user(self, token: str) -> dict:
        """Получение пользователя через токен"""
        return await self._get_user(token)

    async def get_current_admin(self, token: str) -> dict:
        """Получение пользователя через токен со статусом админ"""
        user = await self._get_user(token)
        if user["status"] != Status.ADMIN:
            raise HTTPException(status_code=status.HTTP_403_FORBIDDEN, detail="Not enough permissions")
        return user

    async def _validate_token(self, token: str) -> dict:
        """Валидация токена"""
        payload = decode_access_token(token)
        if payload is None or "sub" not in payload:
            raise HTTPException(
                status_code=status.HTTP_401_UNAUTHORIZED,
                detail="Could not validate credentials",
                headers={"WWW-Authenticate": "Bearer"},
            )
        return payload

    async def _get_user(self, token: str) -> dict:
        payload = await self._validate_token(token)
        user = await self.repo.get(int(payload["sub"]))
        if user is None or not user.is_active:
            raise HTTPException(
                status_code=status.HTTP_401_UNAUTHORIZED,
                detail="Could not validate credentials",
                headers={"WWW-Authenticate": "Bearer"},
            )
        return {
            "id": user.id,
            "name": user.name,
            "email": user.email,
            "team_id": user.team_id,
            "status": user.status,
            "role": payload["role"],
        }
