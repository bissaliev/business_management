from typing import Annotated

from fastapi import Depends, HTTPException, status
from fastapi.security import OAuth2PasswordBearer
from sqlalchemy.ext.asyncio import AsyncSession

from app.clients.user_client import AuthClient
from app.config import settings
from app.database import get_session
from app.repositories.department_repo import DepartmentRepository
from app.schemas.users import EmployeeRole, User
from app.services.department_service import DepartmentService
from app.services.division_service import DivisionService
from app.services.employee_service import EmployeeService
from app.services.structure_services import OrgStructureService

oauth2_scheme = OAuth2PasswordBearer(tokenUrl=settings.URL_TOKEN)


async def org_structure_service(session: Annotated[AsyncSession, Depends(get_session)]):
    return OrgStructureService(session)


OrgStructureServiceDeps = Annotated[OrgStructureService, Depends(org_structure_service)]


async def division_service(session: Annotated[AsyncSession, Depends(get_session)]):
    return DivisionService(session)


DivisionServiceDeps = Annotated[DivisionService, Depends(division_service)]


async def department_service(session: Annotated[AsyncSession, Depends(get_session)]):
    return DepartmentService(session)


DepartmentServiceDeps = Annotated[DepartmentService, Depends(department_service)]


async def employee_service(session: Annotated[AsyncSession, Depends(get_session)]):
    return EmployeeService(session)


EmployeeServiceDeps = Annotated[EmployeeService, Depends(employee_service)]


AuthClientDeps = Annotated[AuthClient, Depends(lambda: AuthClient())]


async def get_current_user(token: Annotated[str, Depends(oauth2_scheme)], user_client: AuthClientDeps) -> User:
    """Проверяет токен через User Service, возвращает данные (id, email, status, team_role)."""
    user_data = await user_client.verify_token(token)
    if not user_data["is_active"]:
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail="Inactive user")
    return User.model_validate(user_data)


CurrentUser = Annotated[User, Depends(get_current_user)]


async def require_admin(user: CurrentUser):
    """
    Разрешает действия только админам руководителям команды (role="менеджер", "админ")"""
    if user.role != EmployeeRole.ADMINISTRATOR:
        raise HTTPException(status_code=status.HTTP_403_FORBIDDEN, detail="Не достаточно прав")
    return user


Admin = Annotated[User, Depends(require_admin)]
AdminDeps = Depends(require_admin)


async def check_admin_team_access(admin: Admin, team_id: int):
    if not (admin.team_id and admin.team_id == team_id):
        raise HTTPException(status_code=status.HTTP_403_FORBIDDEN, detail="Не достаточно прав")


AdminAndAssigned = Depends(check_admin_team_access)


def department_repo(session: Annotated[AsyncSession, Depends(get_session)]):
    return DepartmentRepository(session)


async def check_admin_department_access(
    admin: Admin, department_id: int, repo: Annotated[DepartmentRepository, Depends(department_repo)]
):
    department = await repo.get(department_id)
    if not (admin.team_id and admin.team_id == department.team_id):
        raise HTTPException(status_code=status.HTTP_403_FORBIDDEN, detail="Не достаточно прав")


AdminAndAssignedDepartmentDeps = Depends(check_admin_department_access)
