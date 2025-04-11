from fastapi import APIRouter, HTTPException

from app.routers.dependencies import TeamServiceDeps
from app.schemas.teams import AddEmployee, TeamCreate, TeamResponse

router = APIRouter()


@router.get("/")
async def get_teams(team_service: TeamServiceDeps) -> list[TeamResponse]:
    teams = await team_service.get_teams()
    return teams


@router.post("/")
async def create_team(team_service: TeamServiceDeps, team_data: TeamCreate) -> TeamResponse:
    team = await team_service.create_team(team_data.model_dump())
    return team


@router.get("/{id}")
async def get_team(id: int, team_service: TeamServiceDeps) -> TeamResponse:
    return await team_service.get_one(id)


@router.get("/by-code/{team_code}")
async def get_team_by_code(team_service: TeamServiceDeps, team_code: str) -> TeamResponse:
    team = await team_service.get_team_by_code(team_code)
    if not team:
        raise HTTPException(status_code=404, detail="Team not found")
    return team


@router.post("/{team_id}/add_employee")
async def add_employee(team_service: TeamServiceDeps, team_id: int, employee_data: AddEmployee) -> dict[str, str]:
    await team_service.add_employee(team_id, **employee_data.model_dump(exclude_unset=True))
    return {"message": "Сотрудник добавлен"}
