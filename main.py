import asyncio

from fastapi import FastAPI
from loguru import logger

from app.routes import router
from core.base import Base
from core.database import engine, database
from app.kafka_consumer import AIOConsumer

Base.metadata.create_all(bind=engine)

app = FastAPI()
app.include_router(router=router)


@app.on_event("startup")
async def startup():
    await database.connect()
    logger.debug('Database connected')
    asyncio.create_task(AIOConsumer().listen_kafka())


@app.on_event("shutdown")
async def shutdown():
    await database.disconnect()
    logger.debug('Database disconnected')
