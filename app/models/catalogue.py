from sqlalchemy import Column, Float, Integer, String

from app.core.db.connect import BaseModel


class Catalogue(BaseModel):
    __tablename__ = "catalogue"
    id = Column(Integer, primary_key=True, index=True)
    name = Column(String, nullable=False)
    description = Column(String, nullable=True)
    price = Column(Float, nullable=False)
    stock = Column(Integer, nullable=False, default=0)
    category = Column(String, nullable=True)
