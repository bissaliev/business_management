from fastapi import APIRouter, status

from app.routers.dependencies import AdminDeps, TeamEmployeeServiceDeps
from app.schemas.employees import EmployeeCreate, EmployeeUpdateRole, TeamEmployeeResponse

router = APIRouter()


@router.post(
    "/{team_id}/employees/",
    response_model=TeamEmployeeResponse,
    dependencies=[AdminDeps],
    summary="Регистрация сотрудника",
)
async def create_employee(
    team_id: int, team_emp_service: TeamEmployeeServiceDeps, employee_data: EmployeeCreate
) -> TeamEmployeeResponse:
    return await team_emp_service.create_employee(team_id, employee_data)


@router.get(
    "/{team_id}/employees/",
    response_model=list[TeamEmployeeResponse],
    dependencies=[AdminDeps],
    summary="Получение всех сотрудников определенной команды",
)
async def get_team_employees(team_emp_service: TeamEmployeeServiceDeps, team_id: int) -> list[TeamEmployeeResponse]:
    return await team_emp_service.get_team_employees(team_id)


@router.get(
    "/{team_id}/employees/{employee_id}",
    response_model=TeamEmployeeResponse,
    summary="Получение сотрудника определенной команды",
)
async def get_specific_team_employee(
    team_emp_service: TeamEmployeeServiceDeps, team_id: int, employee_id: int
) -> TeamEmployeeResponse:
    return await team_emp_service.get_specific_team_employee(team_id, employee_id)


@router.patch(
    "/{team_id}/employees/{employee_id}",
    response_model=TeamEmployeeResponse,
    dependencies=[AdminDeps],
    summary="Обновление роли работника",
)
async def update_status(
    team_emp_service: TeamEmployeeServiceDeps, team_id: int, employee_id: int, role: EmployeeUpdateRole
) -> TeamEmployeeResponse:
    return await team_emp_service.update_role(team_id, employee_id, role)


@router.delete(
    "/{team_id}/employees/{employee_id}",
    status_code=status.HTTP_204_NO_CONTENT,
    dependencies=[AdminDeps],
    summary="Удаление сотрудника",
)
async def delete_employee(team_emp_service: TeamEmployeeServiceDeps, team_id: int, employee_id: int) -> None:
    await team_emp_service.delete_employee(team_id, employee_id)
