from typing import Annotated

from fastapi import Depends
from sqlalchemy.ext.asyncio import AsyncSession

from app.database import get_session
from app.services.department_service import DepartmentService
from app.services.employee_manager_service import EmployeeManagerService
from app.services.employee_service import EmployeeService
from app.services.structure_services import OrgStructureService


async def org_structure_service(session: Annotated[AsyncSession, Depends(get_session)]):
    return OrgStructureService(session)


OrgStructureServiceDeps = Annotated[OrgStructureService, Depends(org_structure_service)]


async def department_service(session: Annotated[AsyncSession, Depends(get_session)]):
    return DepartmentService(session)


DepartmentServiceDeps = Annotated[DepartmentService, Depends(department_service)]


async def employee_service(session: Annotated[AsyncSession, Depends(get_session)]):
    return EmployeeService(session)


EmployeeServiceDeps = Annotated[EmployeeService, Depends(employee_service)]


async def employee_manager_service(session: Annotated[AsyncSession, Depends(get_session)]):
    return EmployeeManagerService(session)


EmployeeManagerServiceDeps = Annotated[EmployeeManagerService, Depends(employee_manager_service)]
