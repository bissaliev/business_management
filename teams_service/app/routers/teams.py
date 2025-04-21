from fastapi import APIRouter

from app.routers.dependencies import AdminDeps, TeamServiceDeps
from app.schemas.responses import MessageDelete
from app.schemas.teams import TeamResponse, TeamUpdate

router = APIRouter()


@router.get("/{team_id}", summary="Получение команды по id")
async def get_team(team_id: int, team_service: TeamServiceDeps) -> TeamResponse:
    return await team_service.get_one(team_id)


@router.put("/{team_id}", dependencies=[AdminDeps], summary="Обновление данных команды")
async def update_team(team_service: TeamServiceDeps, team_id: int, update_data: TeamUpdate) -> TeamResponse:
    return await team_service.update_team(team_id, update_data)


@router.delete("/{team_id}", dependencies=[AdminDeps], summary="Удаление команды")
async def delete_team(team_service: TeamServiceDeps, team_id: int) -> MessageDelete:
    await team_service.delete_team(team_id)
    return MessageDelete()
