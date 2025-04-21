from fastapi import HTTPException, status
from sqlalchemy.ext.asyncio import AsyncSession

from app.clients.team_client import TeamServiceClient
from app.models.users import Status, User
from app.repositories.user_repo import UserRepository
from app.schemas.users import Token
from app.security import create_access_token, decode_access_token, get_password_hash, verify_password


class AuthService:
    """Сервис для управления пользователями"""

    def __init__(self, session: AsyncSession):
        self.session = session
        self.repo = UserRepository(session)
        self.team_client = TeamServiceClient()

    async def create(self, user_data: dict):
        """Создание пользователя"""
        if await self.repo.get_user_by_email(user_data["email"]):
            raise HTTPException(status_code=409, detail="Пользователь с таким email существует")

        password = user_data.pop("password")
        hashed_password = get_password_hash(password)
        user_data["hashed_password"] = hashed_password
        team_code = user_data.pop("team_code")
        user = await self.repo.create(**user_data)
        team = await self.team_client.add_employee_to_team(user.id, str(team_code))
        user.team_id = team["team_id"]
        return user

    async def authenticate_user(self, email: str, password: str):
        user = await self.repo.get_user_by_email(email)
        if not user:
            return False
        if not verify_password(password, user.hashed_password):
            return False
        return user

    async def login(self, email: str, password: str) -> Token:
        user = await self.authenticate_user(email, password)
        if not user:
            raise HTTPException(
                status_code=status.HTTP_401_UNAUTHORIZED,
                detail="Incorrect email or password",
                headers={"WWW-Authenticate": "Bearer"},
            )
        if not user.is_active:
            raise HTTPException(status_code=status.HTTP_403_FORBIDDEN, detail="Inactive user")
        data = {"sub": str(user.id), "email": user.email, "status": user.status.value}
        role = await self.team_client.get_employee_role(user.id, user.team_id)
        data |= role
        access_token = create_access_token(data=data)
        return Token(access_token=access_token, token_type="bearer")

    async def get_current_user(self, token: str) -> User:
        """Получение пользователя через токен"""
        credentials_exception = HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Could not validate credentials",
            headers={"WWW-Authenticate": "Bearer"},
        )
        payload = decode_access_token(token)
        if payload is None:
            raise credentials_exception
        user_id: str = payload.get("sub")
        if user_id is None:
            raise credentials_exception
        user = await self.repo.get(int(user_id))
        if user is None or not user.is_active:
            raise credentials_exception
        return user

    async def get_current_admin(self, token: str) -> User:
        user = await self.get_current_user(token)
        if user.status != Status.ADMIN:
            raise HTTPException(status_code=403, detail="Not enough permissions")
        return user

    async def verify_token(self, token: str):
        """
        Проверяет JWT-токен и возвращает данные пользователя.
        """
        user = await self.get_current_user(token)
        role = decode_access_token(token)["role"]

        response = {
            "id": user.id,
            "email": user.email,
            "status": user.status.value,
            "is_active": user.is_active,
            "team_id": user.team_id,
            "role": role,
        }

        return response
