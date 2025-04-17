from typing import Annotated

from fastapi import Depends, HTTPException, status
from fastapi.security import OAuth2PasswordBearer
from sqlalchemy.ext.asyncio import AsyncSession

from app.clients.user_client import UserServiceClient
from app.config import settings
from app.database import get_session
from app.schemas.users import EmployeeRole, User
from app.services.calendar_service import CalendarService
from app.services.event_service import EventService
from app.services.event_webhook_service import EventWebhookService
from app.security import verify_api_key

oauth2_scheme = OAuth2PasswordBearer(tokenUrl=f"{settings.URL_TOKEN}")


async def event_service(session: Annotated[AsyncSession, Depends(get_session)]):
    """Функция для внедрения в зависимости сервис EventService"""
    return EventService(session)


EventServiceDeps = Annotated[EventService, Depends(event_service)]


async def event_webhook_service(session: Annotated[AsyncSession, Depends(get_session)]):
    """Функция для внедрения в зависимости сервис EventWebhookService"""
    return EventWebhookService(session)


EventWebhookServiceDeps = Annotated[EventWebhookService, Depends(event_webhook_service)]


async def calendar_service(session: Annotated[AsyncSession, Depends(get_session)]):
    """Функция для внедрения в зависимости сервис CalendarService"""
    return CalendarService(session)


CalendarServiceDeps = Annotated[CalendarService, Depends(calendar_service)]


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

VerifyApiKey = Depends(verify_api_key)
