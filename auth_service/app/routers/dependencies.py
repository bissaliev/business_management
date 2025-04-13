from typing import Annotated

from fastapi import Depends
from sqlalchemy.ext.asyncio import AsyncSession

from app.clients.team_client import TeamServiceClient
from app.database import get_session
from app.models.users import User
from app.security import oauth2_scheme
from app.services.auth_service import AuthService
from app.services.user_service import UserService


async def user_service(session: Annotated[AsyncSession, Depends(get_session)]):
    return UserService(session)


UserServiceDeps = Annotated[UserService, Depends(user_service)]


async def team_service_client():
    return TeamServiceClient()


TeamServiceClientDeps = Annotated[TeamServiceClient, Depends(team_service_client)]


async def auth_service(session: Annotated[AsyncSession, Depends(get_session)]):
    return AuthService(session)


AuthServiceDeps = Annotated[AuthService, Depends(auth_service)]


async def get_current_user(
    token: Annotated[str, Depends(oauth2_scheme)], session: Annotated[AsyncSession, Depends(get_session)]
):
    auth_service = AuthService(session)
    user = await auth_service.get_current_user(token)
    return user


CurrentUserDeps = Annotated[User, Depends(get_current_user)]
