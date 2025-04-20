from fastapi import APIRouter

from app.routers.dependencies import AdminDeps, OrgStructureServiceDeps
from app.schemas.team_structures import (
    TeamStructureCreate,
    TeamStructureResponse,
    TeamStructureResponseShort,
)

router = APIRouter()


@router.post("/team-structure/", dependencies=[AdminDeps], summary="Создание типа структуры команды")
async def set_team_structure(
    structure: TeamStructureCreate, org_structure_service: OrgStructureServiceDeps
) -> TeamStructureResponseShort:
    new_team_structure = await org_structure_service.create_team_structure(structure)
    return new_team_structure


@router.get("/structure/{team_id}", dependencies=[AdminDeps], summary="Получение иерархии команды")
async def get_team_structure(team_id: int, org_structure_service: OrgStructureServiceDeps) -> TeamStructureResponse:
    hierarchy = await org_structure_service.get_team_structure(team_id)
    return hierarchy


@router.get(
    "/team-structures/", dependencies=[AdminDeps], summary="Получение зарегистрированных организационных структур"
)
async def get_team_structure_all(org_structure_service: OrgStructureServiceDeps) -> list[TeamStructureResponseShort]:
    team_structures = await org_structure_service.get_team_structure_all()
    return team_structures
