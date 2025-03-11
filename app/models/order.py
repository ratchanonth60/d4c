from enum import Enum as PythonEnum

from sqlalchemy import (
    Column,
    DateTime,
    Enum,
    Float,
    ForeignKey,
    Integer,
)
from sqlalchemy.orm import relationship
from sqlalchemy.sql import func

from app.core.db.connect import BaseModel


class OrderStatusEnum(str, PythonEnum):
    PENDING = "pending"
    SHIPPED = "shipped"
    DELIVERED = "delivered"
    CANCELLED = "cancelled"


class Order(BaseModel):
    __tablename__ = "order"
    id = Column(Integer, primary_key=True, index=True)
    customer_id = Column(Integer, ForeignKey("customer.id"), nullable=False)
    shipping_address_id = Column(Integer, ForeignKey("address.id"), nullable=False)
    billing_address_id = Column(Integer, ForeignKey("address.id"), nullable=True)
    total_amount = Column(Float, nullable=False)
    status = Column(Enum(OrderStatusEnum), default=OrderStatusEnum.PENDING)
    created_at = Column(DateTime(timezone=True), server_default=func.now())
    customer = relationship("Customer", back_populates="orders")
    shipping_address = relationship("Address", foreign_keys=[shipping_address_id])  # ที่อยู่สำหรับจัดส่ง
    billing_address = relationship("Address", foreign_keys=[billing_address_id])    # ที่อยู่สำหรับออกใบเสร็จ
