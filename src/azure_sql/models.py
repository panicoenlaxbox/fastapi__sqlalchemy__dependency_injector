from sqlalchemy import Boolean, Column, String
from sqlalchemy.dialects.postgresql import UUID
from sqlalchemy.orm import declarative_base

Base = declarative_base()


class Subscription(Base):
    __tablename__ = "Subscriptions"
    subscription_id = Column(UUID(as_uuid=True), primary_key=True)
    display_name = Column(String)
    enabled = Column(Boolean)
