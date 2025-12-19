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
            logger.info(
                "Connecting to RabbitMQ",
                extra={
                    "host": config.rabbitmq.host,
                    "port": config.rabbitmq.port,
                    "user": config.rabbitmq.user,
                }
            )
            
            self.connection = await aio_pika.connect_robust(config.rabbitmq.url)
            self.channel = await self.connection.channel()
            
            self.exchange = await self.channel.declare_exchange(
                config.queue.exchange,
                ExchangeType.DIRECT,
                durable=True
            )
            
            logger.info(
                "Successfully connected to RabbitMQ",
                extra={
                    "exchange": config.queue.exchange,
                }
            )
            
        except Exception as e:
            logger.exception(
                "Failed to connect to RabbitMQ",
                extra={
                    "host": config.rabbitmq.host,
                    "port": config.rabbitmq.port,
                    "error": str(e),
                }
            )
            raise

    async def disconnect(self) -> None:
        if self.connection and not self.connection.is_closed:
            logger.info("Disconnecting from RabbitMQ")
            await self.connection.close()
            logger.info("Disconnected from RabbitMQ")

    async def publish_image(
        self,
        image_data: bytes,
        filename: str,
        user_id: Optional[str] = None
    ) -> None:
        if not self.channel or not self.exchange:
            raise RuntimeError("RabbitMQ connection not established")

        from uuid import uuid4
        
        file_extension = filename.split(".")[-1] if "." in filename else "jpg"
        if "." in filename:
            file_name_without_ext = ".".join(filename.split(".")[:-1])
        else:
            file_name_without_ext = filename
        
        unique_id = uuid4()
        object_name = f"{user_id}/{file_name_without_ext}_{unique_id}.{file_extension}"

        message_body = {
            "filename": filename,
            "image_data": image_data.hex(),
            "user_id": user_id,
            "object_name": object_name,
        }

        message = Message(
            body=json.dumps(message_body).encode(),
            content_type="application/json",
            delivery_mode=aio_pika.DeliveryMode.PERSISTENT,
        )

        await self.exchange.publish(
            message,
            routing_key=config.queue.image_routing_key,
        )
        logger.debug(
            "Published message to image queue",
            extra={
                "routing_key": config.queue.image_routing_key,
                "image_filename": filename,
                "user_id": user_id,
            }
        )
        
        await self.exchange.publish(
            message,
            routing_key=config.queue.vector_routing_key,
        )
        logger.debug(
            "Published message to vector queue",
            extra={
                "routing_key": config.queue.vector_routing_key,
                "image_filename": filename,
                "user_id": user_id,
            }
        )


rabbitmq_client = RabbitMQClient()

