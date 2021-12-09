from asyncio import sleep
from typing import List

from loguru import logger

from app.models import notifications
from app.schemas import NotificationSchema, NotificationCreate
from core.database import database


class DBHandler:

    @staticmethod
    async def get_user_notifications(user_id: int) -> List[NotificationSchema]:
        """Returns List of NotificationSchema objects for user with user_id"""
        await sleep(5)

        query = (
            notifications.select().where(notifications.c.user_id == user_id,
                                         notifications.c.is_active == True)
        )
        results = await database.fetch_all(query=query)
        logger.debug(f'Checking db for {user_id}')
        logger.debug(
            f'Returns {[NotificationSchema(**dict(result)) for result in results]}')

        return [NotificationSchema(**dict(result)) for result in results]

    @staticmethod
    async def create_notification(
            notification_obj: NotificationCreate) -> NotificationSchema:
        """Creates notification in db and returns NotificationSchema."""

        query = notifications.insert().values(**notification_obj.dict())
        notification_id = await database.execute(query=query)

        return NotificationSchema(**notification_obj.dict(),
                                  id=notification_id)

    @staticmethod
    async def deactivate_notifications(
            notification_list: List[NotificationSchema]) -> None:
        """Sets False to field is_actions for every notification from
        notifications Query"""
        for notification in notification_list:
            query = notifications.update() \
                .where(notifications.c.id == notification.id) \
                .values(is_active=False)
            await database.execute(query=query)
