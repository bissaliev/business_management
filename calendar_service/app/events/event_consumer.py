import asyncio
import json
from typing import Any

import aio_pika
from sqlalchemy.ext.asyncio import AsyncSession

from app.config import settings
from app.database import context_session
from app.logging_config import logger
from app.repositories.event_repo import EventRepository
from app.schemas.producer_messages import (
    MessageType,
    ProducerMessageCreate,
    ProducerMessageDelete,
    ProducerMessageUpdate,
)


class EventConsumer:
    """Консьюмер RabbitMQ"""

    def __init__(self, exchange_name: str, rabbitmq_url: str = settings.RABBITMQ_URL):
        self.rabbitmq_url = rabbitmq_url
        self.exchange_name = exchange_name
        self.connection = None

    async def _connect(self):
        """Открытие подключения"""
        self.connection = await aio_pika.connect_robust(self.rabbitmq_url)

    async def __aenter__(self):
        logger.info("Открыто соединение с брокером")
        await self._connect()
        return self

    async def __aexit__(self, exc_type, exc_value, traceback):
        await self._close()
        logger.info("Соединение с брокером закрыто")
        if exc_type:
            logger.error(f"Возникло исключение {exc_type.__name__}: {exc_value}")
            return True
        return False

    async def _close(self) -> None:
        """Закрытие подключения"""
        if not self.connection.is_closed:
            self.connection.close()

    async def start_consumer(self) -> None:
        """Запуск консьюмера"""
        channel = await self.connection.channel()
        exchange = await channel.declare_exchange(self.exchange_name, aio_pika.ExchangeType.FANOUT)
        queue = await channel.declare_queue(exclusive=True, durable=True)
        await queue.bind(exchange)

        await queue.consume(self.handle_event)
        logger.info("[Calendar Service] Waiting for task events...")
        await asyncio.Future()

    async def handle_event(self, message: aio_pika.IncomingMessage) -> None:
        """Обработчик событий"""
        async with message.process():
            data = json.loads(message.body)
            if data["type"] == MessageType.CREATED:
                event = ProducerMessageCreate.model_validate(data["payload"])
                await self.create_event(**event.model_dump())
            elif data["type"] == MessageType.DELETED:
                event = ProducerMessageDelete.model_validate(data["payload"])
                await self.delete_event(**event.model_dump())
            elif data["type"] == MessageType.UPDATED:
                event = ProducerMessageUpdate.model_validate(data["payload"])
                await self.update_event(**event.model_dump())
            else:
                logger.error(f"Тип события {data['type']} не возможно определить")

    @context_session
    async def create_event(self, session: AsyncSession, **event: Any) -> None:
        """Создание события"""
        repo = EventRepository(session)
        await repo.create(**event)
        await session.commit()
        logger.info(
            f"Создано событие {event['source_id']} с типом {event['event_type']} в календаре для "
            f"пользователя {event['employee_id']}"
        )

    async def delete_event(self, session: AsyncSession, **event: Any) -> None:
        """Удаление события"""
        repo = EventRepository(session)
        await repo.delete_by_source(**event)
        await session.commit()
        logger.info(
            f"Удалено событие {event['source_id']} с типом {event['event_type'].value} из календаре для "
            f"пользователя {event['employee_id']}"
        )

    async def update_event(self, session: AsyncSession, **event: Any) -> None:
        """Обновление события"""
        repo = EventRepository(session)
        source_id = event.pop("source_id")
        event_type = event.pop("event_type")
        employee_id = event.pop("employee_id")
        await repo.update_by_source(source_id, event_type, employee_id, **event)
        await session.commit()
        logger.info(
            f"Обновлено событие {event['source_id']} с типом {event['event_type'].value} из календаре для "
            f"пользователя {event['employee_id']}"
        )


async def main():
    async with EventConsumer() as consumer:
        await consumer.start_consumer()


if __name__ == "__main__":
    asyncio.run(main())
