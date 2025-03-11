from pydantic import BaseModel
from typing import List
from datetime import datetime


class CartLineBase(BaseModel):
    product_id: int
    quantity: int
    price: float
    discount_amount: float = 0.0


class CartLineCreate(CartLineBase):
    pass


class CartLineUpdate(CartLineBase):
    pass


class CartLine(CartLineBase):
    id: int
    cart_id: int
    added_at: datetime

    class Config:
        from_attributes = True

    def calculate_subtotal(self) -> float:
        return self.price * self.quantity

    def calculate_tax(self, tax_rate: float) -> float:
        subtotal_after_discount = self.calculate_subtotal() - self.discount_amount
        return subtotal_after_discount * tax_rate

    def calculate_total(self, tax_rate: float) -> float:
        subtotal_after_discount = self.calculate_subtotal() - self.discount_amount
        tax = self.calculate_tax(tax_rate)
        return subtotal_after_discount + tax


class CartBase(BaseModel):
    customer_id: int


class CartCreate(CartBase):
    pass


class CartUpdate(CartBase):
    pass


class Cart(CartBase):
    id: int
    total_amount: float
    last_updated: datetime
    cart_lines: List[CartLine] = []

    class Config:
        from_attributes = True

    def calculate_cart_total(self, tax_rate: float) -> float:
        total = 0.0
        for cart_line in self.cart_lines:
            total += cart_line.calculate_total(tax_rate)
        self.total_amount = total
        return total
