from pydantic import BaseModel


class NotificationBase(BaseModel):
    """Scheme for reading data"""
    user_id: int
    message: str
    is_active: bool

    class Config:
        orm_mode = True


class NotificationCreate(NotificationBase):
    is_active = True


class NotificationSchema(NotificationBase):
    id: int
