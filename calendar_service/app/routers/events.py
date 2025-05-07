from fastapi import APIRouter, status

from app.routers.dependencies import CurrentUser, EventServiceDeps
from app.schemas.events import EventCreate, EventOut, EventUpdate

router = APIRouter()


@router.post("/", response_model=EventOut, summary="Создание события")
async def create_event(event_data: EventCreate, user: CurrentUser, calendar_service: EventServiceDeps) -> EventOut:
    event = await calendar_service.create_event(event_data, user)
    return event


@router.get("/{event_id}", response_model=EventOut, summary="Получение события")
async def get_event(event_id: int, user: CurrentUser, calendar_service: EventServiceDeps) -> EventOut:
    event = await calendar_service.get_event(event_id, user)
    return event


@router.patch("/{event_id}", response_model=EventOut, summary="Редактирование события")
async def update_event(
    event_id: int, event_data: EventUpdate, user: CurrentUser, calendar_service: EventServiceDeps
) -> EventOut:
    event = await calendar_service.update_event(event_id, event_data, user)
    return event


@router.delete("/{event_id}", status_code=status.HTTP_204_NO_CONTENT, summary="Удаление события")
async def delete_event(event_id: int, user: CurrentUser, calendar_service: EventServiceDeps) -> None:
    await calendar_service.delete_event(event_id, user)
