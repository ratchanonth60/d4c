from typing import Optional

from pydantic import BaseModel

from app.models.address import Tile


class AddressBase(BaseModel):
    title: Tile
    first_name: Optional[str] = None
    last_name: Optional[str] = None
    phone_number: Optional[str] = None
    address_line1: Optional[str] = None
    address_line2: Optional[str] = None
    city: Optional[str] = None
    state: Optional[str] = None
    postal_code: Optional[str] = None
    country: Optional[str] = None


class AddressCreate(AddressBase):
    user_id: int


class AddressUpdate(AddressBase):
    pass


class AddressResponse(AddressBase):
    id: int
    user_id: int

    class Config:
        orm_mode = True
