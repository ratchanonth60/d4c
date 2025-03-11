from sqlalchemy import (
    Boolean,
    Column,
    DateTime,
    Float,
    Integer,
    String,
)

from app.core.db.connect import BaseModel


# INFO:Offer (โปรโมชัน)
class Offer(BaseModel):
    __tablename__ = "offer"
    id = Column(Integer, primary_key=True, index=True)
    name = Column(String, nullable=False)
    discount_percentage = Column(Float, nullable=False)
    start_date = Column(DateTime(timezone=True), nullable=False)
    end_date = Column(DateTime(timezone=True), nullable=False)
    is_active = Column(Boolean, default=True)


class Voucher(BaseModel):
    __tablename__ = "voucher"
    id = Column(Integer, primary_key=True, index=True)
    code = Column(String, unique=True, nullable=False)
    discount_amount = Column(Float, nullable=False)
    expiry_date = Column(DateTime(timezone=True), nullable=False)
    is_used = Column(Boolean, default=False)
