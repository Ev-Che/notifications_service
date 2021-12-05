from sqlalchemy.orm import Session

from . import models
from .schemas import NotificationCreate


def get_notification(db: Session, notification_id: int):
    return db.query(models.Notification).filter(
        models.Notification.id == notification_id).first()


def create_notification(db: Session, notification: NotificationCreate):
    db_notification = models.Notification(**notification.dict())
    db.add(db_notification)
    db.commit()
    db.refresh(db_notification)
    return db_notification
