from typing import Annotated

from fastapi import Depends, HTTPException, status
from fastapi.security import OAuth2PasswordBearer
from sqlalchemy.ext.asyncio import AsyncSession

from app.clients.user_client import AuthClient
from app.config import settings
from app.database import get_session
from app.schemas.users import EmployeeRole, User
from app.services.employee_service import TeamEmployeeService
from app.services.team_news_service import TeamNewsService
from app.services.team_service import TeamService
from app.services.webhook_service import WebHookService

oauth2_scheme = OAuth2PasswordBearer(tokenUrl=settings.URL_TOKEN)


def team_service(session: Annotated[AsyncSession, Depends(get_session)]):
    return TeamService(session)


TeamServiceDeps = Annotated[TeamService, Depends(team_service)]


def team_employee_service(session: Annotated[AsyncSession, Depends(get_session)]):
    return TeamEmployeeService(session)


TeamEmployeeServiceDeps = Annotated[TeamEmployeeService, Depends(team_employee_service)]


def team_news_service(session: Annotated[AsyncSession, Depends(get_session)]):
    return TeamNewsService(session)


TeamNewsServiceDeps = Annotated[TeamNewsService, Depends(team_news_service)]


def webhook_service_service(session: Annotated[AsyncSession, Depends(get_session)]):
    return WebHookService(session)


WebHookServiceDeps = Annotated[WebHookService, Depends(webhook_service_service)]

AuthClientDeps = Annotated[AuthClient, Depends(lambda: AuthClient())]


async def get_current_user(token: Annotated[str, Depends(oauth2_scheme)], user_client: AuthClientDeps) -> User:
    """Проверяет токен через User Service, возвращает данные (id, email, status, team_role)."""
    user_data = await user_client.verify_token(token)
    if not user_data["is_active"]:
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail="Inactive user")
    return User.model_validate(user_data)


CurrentUser = Annotated[User, Depends(get_current_user)]


async def require_admin(team_id: int, user: Annotated[User, Depends(get_current_user)]) -> User:
    """
    Разрешает действия только админам руководителям команды (role="менеджер", "админ")"""
    if not (user.team_id and user.team_id == team_id):
        raise HTTPException(status_code=status.HTTP_403_FORBIDDEN, detail="Не достаточно прав")
    if user.role != EmployeeRole.ADMINISTRATOR:
        raise HTTPException(status_code=status.HTTP_403_FORBIDDEN, detail="Не достаточно прав")
    return user


Admin = Annotated[User, Depends(require_admin)]
AdminDeps = Depends(require_admin)
