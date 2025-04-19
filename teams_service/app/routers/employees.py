from fastapi import APIRouter

from app.routers.dependencies import TeamEmployeeServiceDeps
from app.schemas.employees import EmployeeCreate, EmployeeUpdateRole, TeamEmployeeResponse

router = APIRouter()


@router.post("/employees/", summary="Регистрация сотрудника")
async def create_employee(
    team_emp_service: TeamEmployeeServiceDeps, employee_data: EmployeeCreate
) -> TeamEmployeeResponse:
    return await team_emp_service.create_employee(employee_data)


@router.get("/{team_id}/employees/", summary="Получение всех сотрудников определенной команды")
async def get_team_employees(team_emp_service: TeamEmployeeServiceDeps, team_id: int) -> list[TeamEmployeeResponse]:
    return await team_emp_service.get_team_employees(team_id)


@router.get("/{team_id}/employees/{employee_id}", summary="Получение сотрудника определенной команды")
async def get_specific_team_employee(
    team_emp_service: TeamEmployeeServiceDeps, team_id: int, employee_id: int
) -> TeamEmployeeResponse:
    return await team_emp_service.get_specific_team_employee(team_id, employee_id)


@router.patch("/{team_id}/employees/{employee_id}", summary="Обновление роли работника")
async def update_status(
    team_emp_service: TeamEmployeeServiceDeps, team_id: int, employee_id: int, role: EmployeeUpdateRole
) -> TeamEmployeeResponse:
    return await team_emp_service.update_role(team_id, employee_id, role)


@router.delete("/{team_id}/employees/{employee_id}", summary="Удаление сотрудника")
async def delete_employee(team_emp_service: TeamEmployeeServiceDeps, team_id: int, employee_id: int) -> dict[str, str]:
    await team_emp_service.delete_employee(team_id, employee_id)
    return {"message": "Работник удален"}
