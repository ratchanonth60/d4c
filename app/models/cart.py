from sqlalchemy import Column, DateTime, ForeignKey, Integer, Float
from sqlalchemy.orm import relationship
from sqlalchemy.sql import func

from app.core.db.connect import BaseModel


class Cart(BaseModel):
    __tablename__ = "cart"  # เปลี่ยนจาก "basket" เป็น "cart"
    id = Column(Integer, primary_key=True, index=True)
    customer_id = Column(Integer, ForeignKey("customer.id"), nullable=False)
    customer = relationship(
        "Customer", back_populates="carts"
    )  # เปลี่ยน back_populates จาก "baskets" เป็น "carts"
    product_id = Column(Integer, ForeignKey("catalogue.id"), nullable=False)
    quantity = Column(Integer, nullable=False, default=1)
    added_at = Column(DateTime(timezone=True), server_default=func.now())
    total_amount = Column(Float, nullable=False, default=0.0)
    cart_lines = relationship("CartLine", back_populates="cart", cascade="all, delete-orphan")

class CartLine(BaseModel):
    __tablename__ = "cart_line"
    id = Column(Integer, primary_key=True, index=True)
    cart_id = Column(Integer, ForeignKey("cart.id"), nullable=False)
    product_id = Column(Integer, ForeignKey("catalogue.id"), nullable=False)
    quantity = Column(Integer, nullable=False, default=1)
    price = Column(Float, nullable=False)  
    added_at = Column(DateTime(timezone=True), server_default=func.now())

    cart = relationship("Cart", back_populates="cart_lines")
    product = relationship("Catalogue")


    def calculate_cart_total(self, tax_rate: float) -> float:
        """
        คำนวณยอดรวมทั้งตะกร้าโดยรวมภาษีและส่วนลดจากทุก CartLine
        """
        total = 0.0
        for cart_line in self.cart_lines:
            total += cart_line.calculate_total(tax_rate)
        self.total_amount = total
        return total

    # เมธอดสำหรับใช้ส่วนลดทั้งตะกร้า
    def apply_cart_discount(self, discount_rate: float) -> float:
        """
        ใช้ส่วนลดกับทุก CartLine ในตะกร้า
        """
        total_discount = 0.0
        for cart_line in self.cart_lines:
            total_discount += cart_line.apply_discount(discount_rate)
        self.calculate_cart_total(tax_rate=0.0)  # อัปเดต total_amount หลังหักส่วนลด
        return total_discount

    # เมธอดสำหรับคำนวณน้ำหนักรวมของตะกร้า
    def calculate_cart_weight(self) -> float:
        """
        คำนวณน้ำหนักรวมของสินค้าทั้งหมดในตะกร้า
        """
        total_weight = 0.0
        for cart_line in self.cart_lines:
            total_weight += cart_line.calculate_weight()
        return total_weight
