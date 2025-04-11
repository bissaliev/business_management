from fastapi import APIRouter

from app.routers.dependencies import DivisionServiceDeps
from app.schemas.divisions import DivisionCreate, DivisionResponse, DivisionUpdate

router = APIRouter()


@router.get("/", summary="Получение списка всех дивизий")
async def get_divisions(division_service: DivisionServiceDeps) -> list[DivisionResponse]:
    return await division_service.get_divisions()


@router.post("/", summary="Создание дивизии")
async def create_division(division: DivisionCreate, division_service: DivisionServiceDeps) -> DivisionResponse:
    new_division = await division_service.create_division(division.model_dump())
    return new_division


@router.get("/{id}", summary="Получение дивизии")
async def get_division(id: int, division_service: DivisionServiceDeps) -> DivisionResponse:
    return await division_service.get_division(id)


@router.put("/{id}", summary="Обновление дивизии")
async def update_division(
    id: int, update_data: DivisionUpdate, division_service: DivisionServiceDeps
) -> DivisionResponse:
    return await division_service.update_division(id, update_data.model_dump(exclude_unset=True))
