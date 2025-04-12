from typing import Annotated

from fastapi import Depends
from sqlalchemy.ext.asyncio import AsyncSession

from app.database import get_session
from app.services.employee_service import TeamEmployeeService
from app.services.team_service import TeamService


def team_service(session: Annotated[AsyncSession, Depends(get_session)]):
    return TeamService(session)


TeamServiceDeps = Annotated[TeamService, Depends(team_service)]


def team_employee_service(session: Annotated[AsyncSession, Depends(get_session)]):
    return TeamEmployeeService(session)


TeamEmployeeServiceDeps = Annotated[TeamEmployeeService, Depends(team_employee_service)]
