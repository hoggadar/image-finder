import asyncio
import signal
import logging

from image_loader_service.infrastructure.rabbitmq_consumer import rabbitmq_consumer
from image_loader_service.logger import setup_logger

logger = logging.getLogger(__name__)


async def main():
    setup_logger()
    
    await rabbitmq_consumer.connect()
    
    def signal_handler(sig, frame):
        asyncio.create_task(shutdown())
    
    signal.signal(signal.SIGINT, signal_handler)
    signal.signal(signal.SIGTERM, signal_handler)
    
    try:
        await rabbitmq_consumer.start_consuming()
        
        await asyncio.Event().wait()
    except Exception as e:
        logger.error(f"Error in main loop: {e}")
        raise
    finally:
        await shutdown()


async def shutdown():
    await rabbitmq_consumer.disconnect()


if __name__ == "__main__":
    try:
        asyncio.run(main())
    except KeyboardInterrupt:
        logger.info("Interrupted by user")
    except Exception as e:
        logger.error(f"Fatal error: {e}")
        raise

