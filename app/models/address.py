import enum
from sqlalchemy import  Column, Enum, String
from sqlalchemy.orm import relationship 

from app.core.db.connect import BaseModel


class Tile(str, enum.Enum):
    MR = "MR"
    MRS = "MRS"


class Adress(BaseModel):
    __tablename__ = "address"
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
    user = relationship("User", back_populates="address")

    def __repr__(self) -> str:
        return f"{self.first_name} {self.last_name}"
