from datetime import datetime
from typing import Optional

from pydantic import BaseModel

from app.models.order import OrderStatusEnum

from .address import AddressBase


class OrderBase(BaseModel):
    customer_id: int
    shipping_address_id: int
    billing_address_id: Optional[int] = None
    total_amount: float


class OrderCreate(OrderBase):
    pass


class OrderUpdate(OrderBase):
    pass


class Order(OrderBase):
    id: int
    status: OrderStatusEnum = OrderStatusEnum.PENDING
    created_at: datetime
    shipping_address: AddressBase
    billing_address: Optional[AddressBase] = None

    class Config:
        from_attributes = True
