import asyncio
import json
import os
from asyncio import sleep

from aiokafka import AIOKafkaConsumer
from kafka import KafkaConsumer
from loguru import logger
from pydantic import ValidationError

from app.schemas import NotificationCreate
from core.database import database
from core.db_handler import DBHandler


class Consumer:
    TOPIC = 'notifications'

    def __init__(self):
        self._consumer = KafkaConsumer(
            self.TOPIC,
            bootstrap_servers=os.environ.get('LOCAL_ADDRESS'),
            auto_offset_reset='earliest',
            value_deserializer=self._deserializer
        )

    @staticmethod
    def _deserializer(message):
        return json.loads(message.decode('utf-8'))

    async def listen_kafka(self):
        await database.connect()

        for message in self._consumer:
            logger.debug(f'Got Message: {message.value}')
            try:
                notification = NotificationCreate(**message.value)
            except ValidationError as e:
                logger.error(f'Wrong message structure. {e.errors()}')
                continue

            notification_obj = await DBHandler().create_notification(
                notification_obj=notification)
            logger.info(f'Notifications created {notification_obj}')


# class AIOConsumer:
#     TOPIC = 'notifications'
#
#     def __init__(self):
#         self._consumer = AIOKafkaConsumer(
#             self.TOPIC,
#             bootstrap_servers=os.environ.get('LOCAL_ADDRESS'),
#             auto_offset_reset='earliest',
#             value_deserializer=self._deserializer
#         )
#
#     @staticmethod
#     def _deserializer(message):
#         return json.loads(message.decode('utf-8'))
#
#     async def listen_kafka(self):
#         await self._consumer.start()
#         try:
#             async for message in self._consumer:
#                 logger.debug(f'Got Message: {message.value}')
#                 # try:
#                 #     notification = NotificationCreate(**message.value)
#                 # except ValidationError as e:
#                 #     logger.error(f'Wrong message structure. {e.errors()}')
#                 #     continue
#                 #
#                 # notification_obj = await DBHandler().create_notification(
#                 #     notification_obj=notification)
#                 # logger.info(f'Notifications created {notification_obj}')
#
#         finally:
#             await self._consumer.stop()


if __name__ == '__main__':
    asyncio.run(Consumer().listen_kafka())
