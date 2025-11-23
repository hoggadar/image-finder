import json
import logging
from typing import Optional

import aio_pika
from aio_pika import ExchangeType, Message

from upload_service.config import config

logger = logging.getLogger(__name__)


class RabbitMQClient:
    def __init__(self):
        self.connection: Optional[aio_pika.Connection] = None
        self.channel: Optional[aio_pika.Channel] = None
        self.exchange: Optional[aio_pika.Exchange] = None

    async def connect(self) -> None:
        try:
            self.connection = await aio_pika.connect_robust(config.rabbitmq.url)
            self.channel = await self.connection.channel()
            
            self.exchange = await self.channel.declare_exchange(
                config.queue.exchange,
                ExchangeType.DIRECT,
                durable=True
            )
            
        except Exception as e:
            logger.error(f"Failed to connect to RabbitMQ: {e}")
            raise

    async def disconnect(self) -> None:
        if self.connection and not self.connection.is_closed:
            await self.connection.close()

    async def publish_image(self, image_data: bytes, filename: str, user_id: Optional[str] = None) -> None:
        if not self.channel or not self.exchange:
            raise RuntimeError("RabbitMQ connection not established")

        message_body = {
            "filename": filename,
            "image_data": image_data.hex(),
            "user_id": user_id,
        }

        message = Message(
            body=json.dumps(message_body).encode(),
            content_type="application/json",
            delivery_mode=aio_pika.DeliveryMode.PERSISTENT,
        )

        await self.exchange.publish(
            message,
            routing_key=config.queue.routing_key,
        )


rabbitmq_client = RabbitMQClient()

