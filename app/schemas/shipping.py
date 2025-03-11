from datetime import datetime
from typing import Optional

from pydantic import BaseModel


class ShippingBase(BaseModel):
    order_id: int
    tracking_number: Optional[str] = None
    carrier: Optional[str] = None
    estimated_delivery: Optional[datetime] = None
    status: Optional[str] = None


class ShippingCreate(ShippingBase):
    pass


class ShippingUpdate(ShippingBase):
    pass


class Shipping(ShippingBase):
    id: int

    class Config:
        from_attributes = True
