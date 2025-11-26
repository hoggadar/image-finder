import json
import logging
from typing import Optional

import aio_pika
from aio_pika import ExchangeType
from aio_pika.abc import AbstractIncomingMessage

from vector_loader_service.config import config
from vector_loader_service.infrastructure.clip_client import clip_client
from vector_loader_service.infrastructure.qdrant_client import qdrant_client

logger = logging.getLogger(__name__)


class RabbitMQConsumer:
    def __init__(self):
        self.connection: Optional[aio_pika.Connection] = None
        self.channel: Optional[aio_pika.Channel] = None
        self.queue: Optional[aio_pika.Queue] = None

    async def connect(self) -> None:
        try:
            logger.info(f"Connecting to RabbitMQ at {config.rabbitmq.host}:{config.rabbitmq.port}")
            self.connection = await aio_pika.connect_robust(config.rabbitmq.url)
            self.channel = await self.connection.channel()
            
            await self.channel.set_qos(prefetch_count=1)
            
            exchange = await self.channel.declare_exchange(
                config.queue.exchange,
                ExchangeType.DIRECT,
                durable=True
            )
            logger.info(f"Connected to exchange: {config.queue.exchange}")
            
            self.queue = await self.channel.declare_queue(
                config.queue.vector_queue,
                durable=True
            )
            logger.info(f"Declared queue: {config.queue.vector_queue}")
            
            await self.queue.bind(
                exchange=exchange,
                routing_key=config.queue.vector_routing_key
            )
            logger.info(f"Bound queue with routing key: {config.queue.vector_routing_key}")
            
        except Exception as e:
            logger.error(f"Failed to connect to RabbitMQ: {e}")
            raise

    async def disconnect(self) -> None:
        if self.connection and not self.connection.is_closed:
            await self.connection.close()

    async def process_message(self, message: AbstractIncomingMessage) -> None:
        async with message.process():
            try:
                logger.info("Received message from queue")
                body = json.loads(message.body.decode())
                filename = body.get("filename", "unknown")
                image_data_hex = body.get("image_data")
                user_id = body.get("user_id")
                
                logger.info(f"Processing image: filename={filename}, user_id={user_id}")
                
                if not image_data_hex:
                    logger.error("Message missing image_data")
                    return
                
                if not user_id:
                    logger.error("Message missing user_id")
                    return
                
                image_data = bytes.fromhex(image_data_hex)
                logger.info(f"Decoded image data: {len(image_data)} bytes")
                
                logger.info("Requesting image embedding from CLIP service")
                image_embedding = await clip_client.get_image_embedding(
                    image_data=image_data,
                    filename=filename,
                )
                logger.info(f"Received embedding: dimension={len(image_embedding)}")
                
                file_extension = filename.split(".")[-1] if "." in filename else "jpg"
                if "." in filename:
                    file_name_without_ext = ".".join(filename.split(".")[:-1])
                else:
                    file_name_without_ext = filename
                
                from uuid import uuid4
                unique_id = uuid4()
                object_name = f"{user_id}/{file_name_without_ext}_{unique_id}.{file_extension}"
                
                logger.info(f"Storing vector in Qdrant: object_name={object_name}")
                point_id = qdrant_client.store_vector(
                    vector=image_embedding,
                    user_id=user_id,
                    object_name=object_name,
                    filename=filename,
                )
                logger.info(f"Successfully stored vector with point_id={point_id}")

            except Exception as e:
                logger.error(f"Error processing message: {e}", exc_info=True)
                raise

    async def start_consuming(self) -> None:
        if not self.queue:
            raise RuntimeError("Queue not initialized. Call connect() first")
        
        logger.info("Started consuming messages from queue")
        await self.queue.consume(self.process_message)


rabbitmq_consumer = RabbitMQConsumer()

