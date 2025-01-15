from app.core.config import settings
from app.core.logger import logger

from confluent_kafka import Consumer, KafkaException

# Настройки потребителя
conf = {
    'bootstrap.servers': settings.KAFKA_BOOTSTRAP_SERVERS,
    'group.id': 'my_group_id',     
    'auto.offset.reset': 'earliest'
}

# Создание экземпляра потребителя
consumer = Consumer(conf)

# Подписка на топик
consumer.subscribe([settings.KAFKA_TOPIC])

# Функция для обработки сообщений
def process_message(msg):
    try:
        logger.info(f"[Kafka] Consumer recived message: {msg.value().decode('utf-8')}")
        # Не придумал как обработать.
    except Exception as e:
        logger.info(f"[Kafka] Consumer has error: {e}")

# Основной цикл потребления сообщений
try:
    while True:
        msg = consumer.poll(timeout=1.0)  # Ожидание сообщения в течение 1 секунды
        if msg is None:
            continue
        if msg.error():
            raise KafkaException(msg.error())
        process_message(msg)
except KeyboardInterrupt:
    ...
finally:
    # Закрытие потребителя при завершении работы
    consumer.close()
    logger.info("[Kafka] Consumer stoped")
