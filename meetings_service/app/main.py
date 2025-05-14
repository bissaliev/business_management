from contextlib import asynccontextmanager

from fastapi import FastAPI

from app.clients.rabbitmq.event_publisher import EventPublisher
from app.routers.meetings import router as meeting_router


@asynccontextmanager
async def lifespan(app: FastAPI):
    """Подключение клиента для брокера сообщений RabbitMQ"""
    app.rmq_producer = EventPublisher("calendar_events")
    await app.rmq_producer.start_connection()
    yield
    await app.rmq_producer.disconnect()


app = FastAPI(root_path="/meeting-service", lifespan=lifespan)


app.include_router(meeting_router, prefix="/meetings", tags=["meetings"])
