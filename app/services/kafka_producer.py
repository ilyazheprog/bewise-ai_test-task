from aiokafka import AIOKafkaProducer

producer = AIOKafkaProducer(bootstrap_servers="kafka:9092")

async def send_message(topic, message):
    await producer.start()
    try:
        await producer.send_and_wait(topic, message)
    finally:
        await producer.stop()
