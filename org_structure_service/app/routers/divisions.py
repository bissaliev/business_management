from fastapi import APIRouter, status

from app.routers.dependencies import AdminAndAssigned, DivisionServiceDeps
from app.schemas.divisions import DivisionCreate, DivisionResponse, DivisionUpdate

router = APIRouter()


@router.get(
    "/{team_id}/divisions",
    response_model=list[DivisionResponse],
    summary="Получение списка дивизий определенной команды",
)
async def get_divisions(team_id: int, division_service: DivisionServiceDeps) -> list[DivisionResponse]:
    return await division_service.get_divisions(team_id)


@router.post(
    "/{team_id}/divisions",
    response_model=DivisionResponse,
    dependencies=[AdminAndAssigned],
    summary="Создание дивизии",
)
async def create_division(
    team_id: int, division: DivisionCreate, division_service: DivisionServiceDeps
) -> DivisionResponse:
    new_division = await division_service.create_division(team_id, division)
    return new_division


@router.get("/{team_id}/divisions/{division_id}", response_model=DivisionResponse, summary="Получение дивизии")
async def get_division(team_id: int, division_id: int, division_service: DivisionServiceDeps) -> DivisionResponse:
    return await division_service.get_division(team_id, division_id)


@router.patch(
    "/{team_id}/divisions/{division_id}",
    response_model=DivisionResponse,
    dependencies=[AdminAndAssigned],
    summary="Обновление дивизии",
)
async def update_division(
    team_id: int, division_id: int, update_data: DivisionUpdate, division_service: DivisionServiceDeps
) -> DivisionResponse:
    return await division_service.update_division(team_id, division_id, update_data)


@router.delete(
    "/{team_id}/divisions/{division_id}",
    status_code=status.HTTP_204_NO_CONTENT,
    dependencies=[AdminAndAssigned],
    summary="Удаление дивизии",
)
async def delete_division(team_id: int, division_id: int, division_service: DivisionServiceDeps) -> None:
    await division_service.delete_division(team_id, division_id)
