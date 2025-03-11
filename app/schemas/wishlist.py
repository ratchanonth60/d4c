from datetime import datetime

from pydantic import BaseModel


class WishlistBase(BaseModel):
    customer_id: int
    product_id: int


class WishlistCreate(WishlistBase):
    pass


class WishlistUpdate(WishlistBase):
    pass


class Wishlist(WishlistBase):
    id: int
    added_at: datetime

    class Config:
        from_attributes = True
