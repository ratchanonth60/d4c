from sqlalchemy import (
    Column,
    DateTime,
    ForeignKey,
    Integer,
    String,
)

from app.core.db.connect import BaseModel


class Shipping(BaseModel):
    __tablename__ = "shipping"
    id = Column(Integer, primary_key=True, index=True)
    order_id = Column(Integer, ForeignKey("order.id"), nullable=False)
    tracking_number = Column(String, nullable=True)
    carrier = Column(String, nullable=True)
    estimated_delivery = Column(DateTime(timezone=True), nullable=True)
    status = Column(String, nullable=True)
