from aiokafka import AIOKafkaProducer
from app.core.config import settings
from app.core.logger import logger


producer = AIOKafkaProducer(
    bootstrap_servers=settings.KAFKA_BOOTSTRAP_SERVERS
)

async def start_producer():
    await producer.start()
    logger.info("[Kafka] Producer started")

async def stop_producer():
    await producer.stop()
    logger.info("[Kafka] Producer stoped")

async def send_message(topic: str, message: str):
    await producer.send_and_wait(topic, message.encode('utf-8'))

    logger.info("[Kafka] Producer sended message")