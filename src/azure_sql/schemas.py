import uuid

from pydantic import BaseModel


class Subscription(BaseModel):
    subscription_id: uuid.UUID
    display_name: str
    enabled: bool

    class Config:
        orm_mode = True
