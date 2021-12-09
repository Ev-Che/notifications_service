import sqlalchemy
from core.database import Base


class Notification(Base):

    __tablename__ = 'Notifications'

    id = sqlalchemy.Column(sqlalchemy.Integer, primary_key=True, index=True)
    user_id = sqlalchemy.Column(sqlalchemy.Integer)
    message = sqlalchemy.Column(sqlalchemy.String(255))
    is_active = sqlalchemy.Column(sqlalchemy.Boolean, default=True)


notifications = Notification.__table__
