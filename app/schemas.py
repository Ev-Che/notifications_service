from pydantic import BaseModel


class NotificationBase(BaseModel):
    """Scheme for reading data"""
    user_id: int
    message: str
    is_active: bool


class Notification(NotificationBase):
    """Scheme for returning data"""
    id: int

    class Config:
        """allows the app to take ORM objects and translate them
        into responses automatically"""
        orm_mode = True


class NotificationCreate(NotificationBase):
    pass
