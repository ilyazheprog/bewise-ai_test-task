from fastapi import FastAPI
from app.api.endpoints import app_router
from app.kafka.producer import stop_producer, start_producer
from app.core.logger import logger

app = FastAPI()

@app.on_event("startup")
async def startup_event():
    logger.info("Backend stated")
    await start_producer()

@app.on_event("shutdown")
async def shutdown_event():
    logger.info("Backend stoped")
    await stop_producer()

app.include_router(app_router)