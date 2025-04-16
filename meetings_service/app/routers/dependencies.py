from typing import Annotated

from fastapi import Depends, HTTPException, status
from fastapi.security import OAuth2PasswordBearer
from sqlalchemy.ext.asyncio import AsyncSession

from app.clients.user_client import UserServiceClient
from app.config import settings
from app.database import get_session
from app.schemas.users import EmployeeRole, User
from app.services.meeting_service import MeetingService

BASE_USER_SERVICE_URL = settings.get_user_url()

oauth2_scheme = OAuth2PasswordBearer(tokenUrl=f"{BASE_USER_SERVICE_URL}/auth/token")


async def meeting_service(session: Annotated[AsyncSession, Depends(get_session)]):
    """Функция для внедрения в зависимости сервис MeetingService"""
    return MeetingService(session)


MeetingServiceDeps = Annotated[MeetingService, Depends(meeting_service)]


UserClientDeps = Annotated[UserServiceClient, Depends(lambda: UserServiceClient())]


async def get_current_user(token: Annotated[str, Depends(oauth2_scheme)], user_client: UserClientDeps) -> User:
    """Проверяет токен через User Service, возвращает данные (id, status, team_role)."""
    user_data = await user_client.verify_token(token)
    if not user_data["is_active"]:
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail="Inactive user")
    return User.model_validate(user_data)


CurrentUser = Annotated[User, Depends(get_current_user)]


async def require_manager_or_admin(user: Annotated[User, Depends(get_current_user)]) -> User:
    """
    Разрешает действия только админам руководителям команды (role="менеджер", "админ")"""
    if not user.team_id:
        raise HTTPException(status_code=status.HTTP_403_FORBIDDEN, detail="Не достаточно прав")
    if user.role not in [EmployeeRole.MANAGER, EmployeeRole.ADMINISTRATOR]:
        raise HTTPException(status_code=status.HTTP_403_FORBIDDEN, detail="Не достаточно прав")
    return user


ManagerOrAdmin = Annotated[User, Depends(require_manager_or_admin)]
