from fastapi import FastAPI

from app.routers.calendar import router as calendar_router
from app.routers.events import router as event_router
from app.routers.webhooks import router as webhook_router

app = FastAPI(root_path="/meeting-service")


app.include_router(event_router, prefix="/events", tags=["events"])
app.include_router(calendar_router, prefix="/calendar", tags=["calendar"])
app.include_router(webhook_router, prefix="/webhooks", tags=["webhooks"])
