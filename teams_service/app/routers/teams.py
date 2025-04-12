from fastapi import APIRouter, HTTPException

from app.routers.dependencies import TeamServiceDeps
from app.schemas.teams import TeamCreate, TeamResponse, TeamUpdate

router = APIRouter()


@router.get("/", summary="Получение списка команд")
async def get_teams(team_service: TeamServiceDeps) -> list[TeamResponse]:
    teams = await team_service.get_teams()
    return teams


@router.post("/", summary="Регистрация команды")
async def create_team(team_service: TeamServiceDeps, team_data: TeamCreate) -> TeamResponse:
    team = await team_service.create_team(team_data.model_dump())
    return team


@router.get("/{id}", summary="Получение команды по id")
async def get_team(id: int, team_service: TeamServiceDeps) -> TeamResponse:
    return await team_service.get_one(id)


@router.get("/by-code/{team_code}", summary="Получение команды по team_code")
async def get_team_by_code(team_service: TeamServiceDeps, team_code: str) -> TeamResponse:
    team = await team_service.get_team_by_code(team_code)
    if not team:
        raise HTTPException(status_code=404, detail="Team not found")
    return team


@router.put("/{team_id}", summary="Обновление данных команды")
async def update_team(team_service: TeamServiceDeps, team_id: int, update_data: TeamUpdate) -> TeamResponse:
    return await team_service.update_team(team_id, update_data.model_dump(exclude_unset=True))
