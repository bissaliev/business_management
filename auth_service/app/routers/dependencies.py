from typing import Annotated

from fastapi import Depends
from sqlalchemy.ext.asyncio import AsyncSession

from app.database import get_session
from app.services.user_service import UserService


async def user_service(session: Annotated[AsyncSession, Depends(get_session)]):
    return UserService(session)


UserServiceDeps = Annotated[UserService, Depends(user_service)]
