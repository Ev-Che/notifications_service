from pydantic import BaseModel


class NotificationBase(BaseModel):
    """Scheme for reading data"""
    user_id: int
    message: str
    is_active: bool = True
