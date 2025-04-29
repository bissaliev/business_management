from typing import Annotated

from fastapi import Depends, HTTPException, status
from sqlalchemy.ext.asyncio import AsyncSession

from app.database import get_session
from app.models.users import Status
from app.schemas.users import UserTokenResponse
from app.security import oauth2_scheme
from app.services.auth_service import AuthService
from app.services.user_service import UserService

SessionDeps = Annotated[AsyncSession, Depends(get_session)]
TokenDeps = Annotated[str, Depends(oauth2_scheme)]


async def user_service(session: SessionDeps) -> UserService:
    return UserService(session)


UserServiceDeps = Annotated[UserService, Depends(user_service)]


async def auth_service(session: SessionDeps) -> AuthService:
    return AuthService(session)


AuthServiceDeps = Annotated[AuthService, Depends(auth_service)]


async def get_current_user(token: TokenDeps, auth_service: AuthServiceDeps) -> UserTokenResponse:
    """Получение текущего пользователя"""
    user = await auth_service.get_current_user(token)
    return UserTokenResponse.model_validate(user)


CurrentUserDeps = Annotated[UserTokenResponse, Depends(get_current_user)]


async def get_admin(user: CurrentUserDeps) -> None:
    """Пользователь с доступом администратора"""
    if user.status != Status.ADMIN:
        raise HTTPException(status_code=status.HTTP_403_FORBIDDEN, detail="Not enough permissions")


RequiredAdminDeps = Depends(get_admin)
