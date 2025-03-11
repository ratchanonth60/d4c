from datetime import datetime

from pydantic import BaseModel


class OfferBase(BaseModel):
    name: str
    discount_percentage: float
    start_date: datetime
    end_date: datetime
    is_active: bool = True


class OfferCreate(OfferBase):
    pass


class OfferUpdate(OfferBase):
    pass


class Offer(OfferBase):
    id: int

    class Config:
        from_attributes = True


class VoucherBase(BaseModel):
    code: str
    discount_amount: float
    expiry_date: datetime
    is_used: bool = False


class VoucherCreate(VoucherBase):
    pass


class VoucherUpdate(VoucherBase):
    pass


class Voucher(VoucherBase):
    id: int

    class Config:
        from_attributes = True
