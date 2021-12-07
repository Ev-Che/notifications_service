from sqlalchemy.orm import Query

from app.models import Notification
from app.schemas import NotificationBase
from core.database import SessionLocal


class DBHandler:
    session = SessionLocal()

    def get_user_notifications(self, user_id: int) -> Query:
        """Returns Query obj with all notifications for user with user_id"""
        return self.session.query(Notification).filter(
            Notification.user_id == user_id, Notification.is_active is True)

    def create_notification(self,
                            notification: NotificationBase) -> Notification:
        """Creates and returns Notification obj."""
        db_notification = Notification(**notification.dict())
        self.session.add(db_notification)
        self.session.commit()
        self.session.refresh(db_notification)
        return db_notification

    async def deactivate_notifications(self, notifications: Query) -> None:
        """Sets False to field is_actions for every notification from
        notifications Query"""
        for notification in notifications:
            notification.is_active = False
        self.session.commit()
