from sqlalchemy import (
    Column,
    DateTime,
    ForeignKey,
    Integer,
    String,
)
from sqlalchemy.sql import func

from app.core.db.connect import BaseModel


class Checkout(BaseModel):
    __tablename__ = "checkout"
    id = Column(Integer, primary_key=True, index=True)
    order_id = Column(Integer, ForeignKey("order.id"), nullable=False)
    status = Column(String, nullable=False, default="in_progress")
    created_at = Column(DateTime(timezone=True), server_default=func.now())
