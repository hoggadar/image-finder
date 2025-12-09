import json
import logging
from typing import Optional
from uuid import uuid4

import aio_pika
from aio_pika import ExchangeType
from aio_pika.abc import AbstractIncomingMessage

from vector_loader_service.app.dependency import get_clip_api_service
from vector_loader_service.config import config
from vector_loader_service.infrastructure.qdrant_client import qdrant_client

logger = logging.getLogger(__name__)


class RabbitMQConsumer:
    def __init__(self):
        self.connection: Optional[aio_pika.Connection] = None
        self.channel: Optional[aio_pika.Channel] = None
        self.queue: Optional[aio_pika.Queue] = None
        self.clip_service = get_clip_api_service()

    async def connect(self) -> None:
        try:
            logger.info(
                "Connecting to RabbitMQ",
                extra={
                    "host": config.rabbitmq.host,
                    "port": config.rabbitmq.port,
                }
            )
            self.connection = await aio_pika.connect_robust(config.rabbitmq.url)
            self.channel = await self.connection.channel()
            
            await self.channel.set_qos(prefetch_count=1)
            
            exchange = await self.channel.declare_exchange(
                config.queue.exchange,
                ExchangeType.DIRECT,
                durable=True
            )
            logger.info(
                "Connected to exchange",
                extra={"exchange": config.queue.exchange}
            )
            
            self.queue = await self.channel.declare_queue(
                config.queue.vector_queue,
                durable=True
            )
            logger.info(
                "Declared queue",
                extra={"queue": config.queue.vector_queue}
            )
            
            await self.queue.bind(
                exchange=exchange,
                routing_key=config.queue.vector_routing_key
            )
            logger.info(
                "Bound queue with routing key",
                extra={"routing_key": config.queue.vector_routing_key}
            )
            
        except Exception as e:
            logger.exception(
                "Failed to connect to RabbitMQ",
                extra={"error": str(e)}
            )
            raise

    async def disconnect(self) -> None:
        if self.connection and not self.connection.is_closed:
            await self.connection.close()

    async def process_message(self, message: AbstractIncomingMessage) -> None:
        async with message.process():
            try:
                logger.info("Received message from queue")
                body = json.loads(message.body.decode())
                image_filename = body.get("filename", "unknown")
                image_data_hex = body.get("image_data")
                user_id = body.get("user_id")
                
                logger.info(
                    "Processing image",
                    extra={
                        "image_filename": image_filename,
                        "user_id": user_id,
                    }
                )
                
                if not image_data_hex:
                    logger.error("Message missing image_data")
                    return
                
                if not user_id:
                    logger.error("Message missing user_id")
                    return
                
                image_data = bytes.fromhex(image_data_hex)
                logger.info(
                    "Decoded image data",
                    extra={"size": len(image_data)}
                )
                
                logger.info("Requesting image embedding from CLIP service")
                image_embedding = await self.clip_service.get_image_embedding(
                    image_data=image_data,
                    image_filename=image_filename,
                )
                logger.info(
                    "Received embedding from CLIP service",
                    extra={"dimension": len(image_embedding)}
                )
                
                # Use object_name from message if provided, otherwise generate new one
                object_name = body.get("object_name")
                if not object_name:
                    # Fallback: generate object name if not provided in message
                    file_extension = image_filename.split(".")[-1] if "." in image_filename else "jpg"
                    if "." in image_filename:
                        file_name_without_ext = ".".join(image_filename.split(".")[:-1])
                    else:
                        file_name_without_ext = image_filename
                    
                    unique_id = uuid4()
                    object_name = f"{user_id}/{file_name_without_ext}_{unique_id}.{file_extension}"
                
                logger.info(
                    "Storing vector in Qdrant",
                    extra={"object_name": object_name}
                )
                point_id = qdrant_client.store_vector(
                    vector=image_embedding,
                    user_id=user_id,
                    object_name=object_name,
                    image_filename=image_filename,
                )
                logger.info(
                    "Successfully stored vector in Qdrant",
                    extra={"point_id": point_id}
                )

            except Exception as e:
                logger.exception(
                    "Error processing message",
                    extra={"error": str(e)}
                )
                raise

    async def start_consuming(self) -> None:
        if not self.queue:
            raise RuntimeError("Queue not initialized. Call connect() first")
        
        logger.info("Started consuming messages from queue")
        await self.queue.consume(self.process_message)


rabbitmq_consumer = RabbitMQConsumer()

