import json

import aio_pika

from app.config import settings
from app.logging_config import logger


class EventPublisher:
    """
    Класс для публикации событий в RabbitMQ через Fanout exchange.

    Атрибуты:
        exchange_name (str): Имя exchange, куда публикуются события.
        rabbitmq_url (str): URL для подключения к RabbitMQ.
        connection (AbstractRobustConnection | None): Надежное соединение с RabbitMQ.
        channel (AbstractRobustChannel | None): Канал для обмена сообщениями.
        exchange (AbstractExchange | None): Exchange, в который будут отправляться события.
    """

    def __init__(self, exchange_name: str, rabbitmq_url: str = settings.RABBITMQ_URL):
        self.rabbitmq_url = rabbitmq_url
        self.exchange_name = exchange_name

        self.connection: aio_pika.abc.AbstractRobustConnection | None = None
        self.channel: aio_pika.abc.AbstractRobustChannel | None = None
        self.exchange: aio_pika.abc.AbstractExchange | None = None

    async def start_connection(self) -> None:
        """
        Устанавливает соединение, открывает канал и объявляет exchange.
        """
        logger.info("Инициализация соединения с RabbitMQ")
        self.connection = await aio_pika.connect_robust(url=self.rabbitmq_url)
        logger.info("Соединение установлено")

        logger.info("Открытие нового канала")
        self.channel = await self.connection.channel()
        logger.info("Канал открыт")

        logger.info(f"Объявление exchange '{self.exchange_name}' с типом FANOUT")
        self.exchange = await self.channel.declare_exchange(name=self.exchange_name, type=aio_pika.ExchangeType.FANOUT)
        logger.info(f"Exchange '{self.exchange_name}' успешно объявлен")

    async def publish(self, event: dict) -> None:
        """
        Публикует событие в exchange.

        Args:
            event (dict): Событие для отправки. Ожидается структура с полями 'type' и 'payload'.
        """
        message = aio_pika.Message(body=json.dumps(event).encode(), delivery_mode=aio_pika.DeliveryMode.PERSISTENT)
        await self.exchange.publish(message, routing_key="")
        logger.info(f"Опубликованное событие {event['type']} для задачи {event['payload']['source_id']}")

    async def disconnect(self):
        """
        Закрывает соединение с RabbitMQ, если оно было открыто.
        """
        try:
            if self.connection and not self.connection.is_closed:
                await self.connection.close()
                logger.info("Соединение с RabbitMQ закрыто")
        except Exception as e:
            logger.error("Ошибка при закрытии соединения с RabbitMQ", exc_info=e)
