import asyncio
from contextlib import asynccontextmanager

from fastapi import FastAPI

from app.events.event_consumer import EventConsumer
from app.logging_config import logger
from app.routers.calendar import router as calendar_router
from app.routers.events import router as event_router
from app.routers.webhooks import router as webhook_router


@asynccontextmanager
async def lifespan(app: FastAPI):
    async with EventConsumer("calendar_events") as consumer:
        task = asyncio.create_task(consumer.start_consumer())
        await asyncio.sleep(0)
        yield
        task.cancel()
        try:
            await task
        except asyncio.CancelledError:
            logger.info("Фоновая задача RabbitMQ остановлена")


app = FastAPI(root_path="/calendar-service", lifespan=lifespan)


app.include_router(event_router, prefix="/events", tags=["events"])
app.include_router(calendar_router, prefix="/calendar", tags=["calendar"])
app.include_router(webhook_router, prefix="/webhooks", tags=["webhooks"])
