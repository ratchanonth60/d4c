from pydantic import BaseModel
from datetime import datetime

from app.models.payment import PaymentStatusEnum


class PaymentBase(BaseModel):
    order_id: int
    amount: float
    payment_method: str
    status: PaymentStatusEnum = PaymentStatusEnum.PENDING


class PaymentCreate(PaymentBase):
    pass


class PaymentUpdate(BaseModel):
    status: PaymentStatusEnum


class Payment(PaymentBase):
    id: int
    created_at: datetime

    class Config:
        from_attributes = True
