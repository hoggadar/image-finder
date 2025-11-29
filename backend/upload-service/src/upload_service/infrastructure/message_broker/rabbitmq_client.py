import json
import logging
from typing import Optional

import aio_pika
from aio_pika import ExchangeType, Message

from upload_service.config import config


logger = logging.getLogger(__name__)


class RabbitMQClient:
    """RabbitMQ client for publishing image upload messages."""
    
    def __init__(self):
        self.connection: Optional[aio_pika.Connection] = None
        self.channel: Optional[aio_pika.Channel] = None
        self.exchange: Optional[aio_pika.Exchange] = None

    async def connect(self) -> None:
        """Establish connection to RabbitMQ and declare exchange."""
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
        """Close RabbitMQ connection."""
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
        """
        Publish image to message queue for processing.
        
        Args:
            image_data: Raw image bytes
            filename: Original filename
            user_id: ID of user who uploaded the image
            
        Raises:
            RuntimeError: If RabbitMQ connection is not established
        """
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

        # Publish to image queue (for storage in MinIO)
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
        
        # Publish to vector queue (for CLIP embeddings generation)
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


# Global singleton instance
rabbitmq_client = RabbitMQClient()

