from enum import Enum as PythonEnum

from sqlalchemy import Column, DateTime, Enum, Float, ForeignKey, Integer, String
from sqlalchemy.sql import func

from app.core.db.connect import BaseModel


class PaymentStatusEnum(str, PythonEnum):
    PENDING = "pending"
    COMPLETED = "completed"
    FAILED = "failed"


class Payment(BaseModel):
    __tablename__ = "payment"
    id = Column(Integer, primary_key=True, index=True)
    order_id = Column(Integer, ForeignKey("order.id"), nullable=False)
    amount = Column(Float, nullable=False)
    payment_method = Column(String, nullable=False)
    status = Column(Enum(PaymentStatusEnum), default=PaymentStatusEnum.PENDING)
    created_at = Column(DateTime(timezone=True), server_default=func.now())
