from typing import List

from .address import AddressBase
from .cart import Cart
from .order import Order
from .user import User, UserBase, UserCreate
from .wishlist import Wishlist


class CustomerBase(UserBase):
    pass


class CustomerCreate(UserCreate):
    pass


class CustomerUpdate(UserBase):
    pass


class Customer(User):
    addresses: List[AddressBase] = []
    carts: List[Cart] = []
    orders: List["Order"] = []
    wishlists: List["Wishlist"] = []

    class Config:
        from_attributes = True
