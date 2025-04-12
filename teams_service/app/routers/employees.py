from fastapi import APIRouter

from app.routers.dependencies import TeamEmployeeServiceDeps
from app.schemas.teams import AddEmployee, EmployeeUpdateRole, TeamEmployeeResponse

router = APIRouter()


@router.get("/{team_id}/employees/", summary="Получение всех сотрудников определенной команды")
async def get_team_employees(team_emp_service: TeamEmployeeServiceDeps, team_id: int) -> list[TeamEmployeeResponse]:
    return await team_emp_service.get_team_employees(team_id)


@router.post("/{team_id}/employees/", summary="Добавление сотрудника в команду")
async def add_employee_to_team(
    team_emp_service: TeamEmployeeServiceDeps, team_id: int, employee_data: AddEmployee
) -> TeamEmployeeResponse:
    return await team_emp_service.add_employee_to_team(team_id, employee_data.model_dump())


@router.get("/{team_id}/employees/{employee_id}", summary="Получение сотрудника определенной команды")
async def get_specific_team_employee(
    team_emp_service: TeamEmployeeServiceDeps, team_id: int, employee_id: int
) -> TeamEmployeeResponse:
    return await team_emp_service.get_specific_team_employee(team_id, employee_id)


@router.patch("/{team_id}/employees/{employee_id}", summary="Обновление роли работника")
async def update_status(
    team_emp_service: TeamEmployeeServiceDeps, team_id: int, employee_id: int, role: EmployeeUpdateRole
) -> TeamEmployeeResponse:
    return await team_emp_service.update_role(team_id, employee_id, role.model_dump())
