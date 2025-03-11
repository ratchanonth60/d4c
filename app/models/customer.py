from sqlalchemy import (
    Column,
    ForeignKey,
    Integer,
)
from sqlalchemy.orm import relationship

from .user import User


class Customer(User):  # สืบทอดจาก User
    __tablename__ = "customer"  # ใช้ตารางแยกสำหรับ Customer
    __mapper_args__ = {"polymorphic_identity": "customer"}  # ระบุว่าเป็น subtype

    id = Column(Integer, ForeignKey("users.id"), primary_key=True)  # ใช้ id จาก User
    addresses = relationship("Address", back_populates="customer")
    carts = relationship("Cart", back_populates="customer")
    orders = relationship("Order", back_populates="customer")
    wishlists = relationship("Wishlist", back_populates="customer")
