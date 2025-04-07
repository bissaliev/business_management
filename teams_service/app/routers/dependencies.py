from app.database import get_session
from fastapi import Depends
from typing import Annotated
from sqlalchemy.ext.asyncio import AsyncSession
from app.services import TeamService


def team_service(session: Annotated[AsyncSession, Depends(get_session)]):
    return TeamService(session)


TeamServiceDeps = Annotated[TeamService, Depends(team_service)]
