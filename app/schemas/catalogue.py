from typing import Optional

from pydantic import BaseModel


class CatalogueBase(BaseModel):
    name: str
    description: Optional[str] = None
    price: float
    stock: int
    category: Optional[str] = None


class CatalogueCreate(CatalogueBase):
    pass


class CatalogueUpdate(CatalogueBase):
    pass


class Catalogue(CatalogueBase):
    id: int

    class Config:
        from_attributes = True
