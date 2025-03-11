import enum

from sqlalchemy import Column, Enum, ForeignKey, Integer, String
from sqlalchemy.orm import relationship

from app.core.db.connect import BaseModel


class Tile(str, enum.Enum):
    MR = "MR"
    MRS = "MRS"


class Address(BaseModel):
    __tablename__ = "address"
    id = Column(Integer, primary_key=True, index=True)
    title = Column(Enum(Tile), nullable=False)
    first_name = Column(String, nullable=True)
    last_name = Column(String, nullable=True)
    phone_number = Column(String, nullable=True)
    address_line1 = Column(String, nullable=True)
    address_line2 = Column(String, nullable=True)
    city = Column(String, nullable=True)
    state = Column(String, nullable=True)
    postal_code = Column(String, nullable=True)
    country = Column(String, nullable=True)
    customer_id = Column(Integer, ForeignKey("customer.id"))
    customer = relationship("Customer", back_populates="addresses")

    def __repr__(self) -> str:
        return f"{self.first_name} {self.last_name}"
