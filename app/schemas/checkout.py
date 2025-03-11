from datetime import datetime

from pydantic import BaseModel


class CheckoutBase(BaseModel):
    order_id: int
    status: str = "in_progress"


class CheckoutCreate(CheckoutBase):
    pass


class CheckoutUpdate(CheckoutBase):
    pass


class Checkout(CheckoutBase):
    id: int
    created_at: datetime

    class Config:
        from_attributes = True
