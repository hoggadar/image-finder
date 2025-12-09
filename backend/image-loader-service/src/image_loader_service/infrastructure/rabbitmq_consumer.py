import json
import logging
from typing import Optional

import aio_pika
from aio_pika import ExchangeType
from aio_pika.abc import AbstractIncomingMessage

from image_loader_service.config import config
from image_loader_service.infrastructure.minio_client import minio_client

logger = logging.getLogger(__name__)


class RabbitMQConsumer:
    def __init__(self):
        self.connection: Optional[aio_pika.Connection] = None
        self.channel: Optional[aio_pika.Channel] = None
        self.queue: Optional[aio_pika.Queue] = None

    async def connect(self) -> None:
        try:
            self.connection = await aio_pika.connect_robust(config.rabbitmq.url)
            self.channel = await self.connection.channel()
            
            await self.channel.set_qos(prefetch_count=1)
            
            exchange = await self.channel.declare_exchange(
                config.queue.exchange,
                ExchangeType.DIRECT,
                durable=True
            )
            
            self.queue = await self.channel.declare_queue(
                config.queue.image_queue,
                durable=True
            )
            
            await self.queue.bind(
                exchange=exchange,
                routing_key=config.queue.image_routing_key
            )
            
        except Exception as e:
            logger.error(f"Failed to connect to RabbitMQ: {e}")
            raise

    async def disconnect(self) -> None:
        if self.connection and not self.connection.is_closed:
            await self.connection.close()

    async def process_message(self, message: AbstractIncomingMessage) -> None:
        async with message.process():
            try:
                body = json.loads(message.body.decode())
                filename = body.get("filename", "unknown")
                image_data_hex = body.get("image_data")
                user_id = body.get("user_id")
                
                if not image_data_hex:
                    logger.error("Message missing image_data")
                    return
                
                if not user_id:
                    logger.error("Message missing user_id")
                    return
                
                image_data = bytes.fromhex(image_data_hex)
                
                # Use object_name from message if provided, otherwise generate new one
                object_name = body.get("object_name")
                
                object_name = minio_client.upload_image(
                    image_data=image_data,
                    filename=filename,
                    user_id=user_id,
                    object_name=object_name,
                )

            except Exception as e:
                logger.error(f"Error processing message: {e}")
                raise

    async def start_consuming(self) -> None:
        if not self.queue:
            raise RuntimeError("Queue not initialized. Call connect() first")
        
        await self.queue.consume(self.process_message)


rabbitmq_consumer = RabbitMQConsumer()

