import asyncio
import logging
import os
import sys

import aio_pika
from aio_pika import ExchangeType

logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s [%(levelname)s] %(name)s: %(message)s"
)
logger = logging.getLogger(__name__)


RABBITMQ_CONFIG = {
    "exchanges": [
        {
            "name": "image_exchange",
            "type": ExchangeType.DIRECT,
            "durable": True,
        },
    ],
    "queues": [
        {
            "name": "image_upload_queue",
            "durable": True,
            "arguments": {},
        },
        {
            "name": "vector_upload_queue",
            "durable": True,
            "arguments": {},
        },
    ],
    "bindings": [
        {
            "queue": "image_upload_queue",
            "exchange": "image_exchange",
            "routing_key": "image.upload",
        },
        {
            "queue": "vector_upload_queue",
            "exchange": "image_exchange",
            "routing_key": "vector.upload",
        },
    ],
}


async def init_rabbitmq():
    rabbitmq_host = os.getenv("RABBITMQ_HOST", "localhost")
    rabbitmq_port = int(os.getenv("RABBITMQ_PORT", "5672"))
    rabbitmq_user = os.getenv("RABBITMQ_USER", "guest")
    rabbitmq_password = os.getenv("RABBITMQ_PASSWORD", "guest")
    rabbitmq_vhost = os.getenv("RABBITMQ_VHOST", "/")
    
    url = f"amqp://{rabbitmq_user}:{rabbitmq_password}@{rabbitmq_host}:{rabbitmq_port}/{rabbitmq_vhost}"
    
    logger.info(f"Connecting to RabbitMQ at {rabbitmq_host}:{rabbitmq_port}")
    
    try:
        connection = await aio_pika.connect_robust(url)
        channel = await connection.channel()
        
        exchanges = {}
        for exchange_config in RABBITMQ_CONFIG["exchanges"]:
            exchange = await channel.declare_exchange(
                name=exchange_config["name"],
                type=exchange_config["type"],
                durable=exchange_config["durable"],
            )
            exchanges[exchange_config["name"]] = exchange
        
        queues = {}
        for queue_config in RABBITMQ_CONFIG["queues"]:
            queue = await channel.declare_queue(
                name=queue_config["name"],
                durable=queue_config["durable"],
                arguments=queue_config.get("arguments", {}),
            )
            queues[queue_config["name"]] = queue
        
        for binding_config in RABBITMQ_CONFIG["bindings"]:
            queue = queues[binding_config["queue"]]
            exchange = exchanges[binding_config["exchange"]]
            await queue.bind(
                exchange=exchange,
                routing_key=binding_config["routing_key"],
            )
        
        await connection.close()
        
    except Exception as e:
        sys.exit(1)


if __name__ == "__main__":
    asyncio.run(init_rabbitmq())

