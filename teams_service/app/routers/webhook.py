from fastapi import APIRouter, Depends

from app.routers.dependencies import WebHookServiceDeps
from app.schemas.employees import TeamEmployeeResponse
from app.schemas.users import EmployeeCreate
from app.security import verify_api_key

router = APIRouter()


@router.post("/add_employee/", dependencies=[Depends(verify_api_key)], summary="Регистрация в команде по team_code")
async def add_employee_to_team(team_service: WebHookServiceDeps, new_employee: EmployeeCreate) -> TeamEmployeeResponse:
    return await team_service.add_employee(new_employee)
