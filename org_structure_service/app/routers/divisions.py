from fastapi import APIRouter

from app.routers.dependencies import AdminAndAssigned, DivisionServiceDeps
from app.schemas.divisions import DivisionCreate, DivisionResponse, DivisionUpdate
from app.schemas.response import MessageDelete

router = APIRouter(dependencies=[AdminAndAssigned])


@router.get("/{team_id}/divisions", summary="Получение списка дивизий определенной команды")
async def get_divisions(team_id: int, division_service: DivisionServiceDeps) -> list[DivisionResponse]:
    return await division_service.get_divisions(team_id)


@router.post("/{team_id}/divisions", summary="Создание дивизии")
async def create_division(
    team_id: int, division: DivisionCreate, division_service: DivisionServiceDeps
) -> DivisionResponse:
    new_division = await division_service.create_division(team_id, division)
    return new_division


@router.get("/{team_id}/divisions/{division_id}", summary="Получение дивизии")
async def get_division(team_id: int, division_id: int, division_service: DivisionServiceDeps) -> DivisionResponse:
    return await division_service.get_division(team_id, division_id)


@router.patch("/{team_id}/divisions/{division_id}", summary="Обновление дивизии")
async def update_division(
    team_id: int, division_id: int, update_data: DivisionUpdate, division_service: DivisionServiceDeps
) -> DivisionResponse:
    return await division_service.update_division(team_id, division_id, update_data)


@router.delete("/{team_id}/divisions/{division_id}", summary="Удаление дивизии")
async def delete_division(team_id: int, division_id: int, division_service: DivisionServiceDeps) -> MessageDelete:
    await division_service.delete_division(team_id, division_id)
    return MessageDelete()
