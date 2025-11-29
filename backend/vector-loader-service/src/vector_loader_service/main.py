import asyncio
import signal
import logging

from vector_loader_service.infrastructure.rabbitmq_consumer import rabbitmq_consumer
from vector_loader_service.logger import setup_logger

logger = logging.getLogger(__name__)


async def main():
    setup_logger()
    logger.info("=" * 60)
    logger.info("Starting Vector Loader Service")
    logger.info("=" * 60)
    
    try:
        await rabbitmq_consumer.connect()
        logger.info("RabbitMQ connection established successfully")
    except Exception as e:
        logger.error(f"Failed to connect to RabbitMQ: {e}", exc_info=True)
        raise
    
    def signal_handler(sig, frame):
        asyncio.create_task(shutdown())
    
    signal.signal(signal.SIGINT, signal_handler)
    signal.signal(signal.SIGTERM, signal_handler)
    
    try:
        await rabbitmq_consumer.start_consuming()
        logger.info("Vector Loader Service is ready and waiting for messages")
        
        await asyncio.Event().wait()
    except Exception as e:
        logger.error(f"Error in main loop: {e}", exc_info=True)
        raise
    finally:
        await shutdown()


async def shutdown():
    logger.info("Shutting down Vector Loader Service")
    await rabbitmq_consumer.disconnect()
    logger.info("Disconnected from RabbitMQ")


if __name__ == "__main__":
    try:
        asyncio.run(main())
    except KeyboardInterrupt:
        logger.info("Interrupted by user")
    except Exception as e:
        logger.error(f"Fatal error: {e}")
        raise

