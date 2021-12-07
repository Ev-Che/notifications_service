import json
import os

from kafka import KafkaConsumer
from loguru import logger
from pydantic import ValidationError

from app.schemas import NotificationBase
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

    def listen_kafka(self):
        for message in self._consumer:
            logger.debug(f'Got Message: {message.value}')
            try:
                notification = NotificationBase(**message.value)
            except ValidationError as e:
                logger.error(f'Wrong message structure. {e.errors()}')
            notification_obj = DBHandler().create_notification(
                notification=notification)
            logger.info(f'Notifications created {notification_obj}')


if __name__ == '__main__':
    Consumer().listen_kafka()
