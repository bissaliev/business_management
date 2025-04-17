from typing import Annotated

from fastapi import APIRouter, Query, status
from fastapi.responses import JSONResponse

from app.routers.dependencies import EventWebhookServiceDeps, VerifyApiKey
from app.schemas.event_webhooks import EventDeleteParams, EventParams, NewEventHook

router = APIRouter(dependencies=[VerifyApiKey])


@router.post("/new-event", summary="Вебхук для создание события")
async def handle_new_event_webhook(event_data: NewEventHook, event_service: EventWebhookServiceDeps):
    await event_service.create_event(event_data)
    return JSONResponse(content={"status": "success"}, status_code=status.HTTP_200_OK)


@router.get("/verify-event", summary="Вебхук проверяет наличие события в определенный период")
async def handle_verify_event_webhook(
    event_data: Annotated[EventParams, Query()], event_service: EventWebhookServiceDeps
):
    await event_service.verify_event(event_data)
    return JSONResponse(content={"exists": True}, status_code=status.HTTP_200_OK)


@router.delete("/remove-event", summary="Вебхук для удаления события")
async def handle_delete_event_webhook(
    event_data: Annotated[EventDeleteParams, Query()], event_service: EventWebhookServiceDeps
):
    await event_service.delete_event(event_data)
    return JSONResponse(content={"status": "success"}, status_code=status.HTTP_200_OK)
