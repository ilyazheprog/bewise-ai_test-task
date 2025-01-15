import os

class Settings:
    DATABASE_URL = os.getenv("DATABASE_URL", "postgresql+asyncpg://user:password@db/applications")
    KAFKA_BOOTSTRAP_SERVERS = os.getenv("KAFKA_BOOTSTRAP_SERVERS", "localhost:9092")
    KAFKA_TOPIC = os.getenv("KAFKA_TOPIC", "my_topic")
    MAX_CONNECTIONS = int(os.getenv("MAX_CONNECTIONS", 10))
    MIN_CONNECTIONS = int(os.getenv("MIN_CONNECTIONS", 1))

settings = Settings()
