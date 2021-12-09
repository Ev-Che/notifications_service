import json
import os

from aiokafka import AIOKafkaConsumer
from loguru import logger
from pydantic import ValidationError

from app.schemas import NotificationCreate
from core.db_handler import DBHandler


class AIOConsumer:
    TOPIC = 'notifications'

    def __init__(self):
        self._consumer = AIOKafkaConsumer(
            self.TOPIC,
            bootstrap_servers=os.environ.get('LOCAL_ADDRESS'),
            auto_offset_reset='earliest',
            value_deserializer=self._deserializer
        )

    @staticmethod
    def _deserializer(message):
        return json.loads(message.decode('utf-8'))

    async def listen_kafka(self):
        await self._consumer.start()
        try:
            async for message in self._consumer:
                logger.debug(f'Got Message: {message.value}')
                try:
                    await self._write_to_db(message)
                except ValidationError as e:
                    logger.error(f'Wrong message structure. {e.errors()}')
                    continue
        finally:
            await self._consumer.stop()

    @staticmethod
    async def _write_to_db(message):
        try:
            notification = NotificationCreate(**message.value)
        except ValidationError as e:
            logger.error(f'Wrong message structure. {e.errors()}')
            raise e

        notification_obj = await DBHandler().create_notification(
            notification_obj=notification)
        logger.info(f'Notification was written {notification_obj}')
