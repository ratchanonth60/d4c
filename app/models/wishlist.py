from sqlalchemy import (
    Column,
    DateTime,
    ForeignKey,
    Integer,
)
from sqlalchemy.orm import relationship
from sqlalchemy.sql import func

from app.core.db.connect import BaseModel


class Wishlist(BaseModel):
    __tablename__ = "wishlists"
    id = Column(Integer, primary_key=True, index=True)
    customer_id = Column(Integer, ForeignKey("customer.id"), nullable=False)
    product_id = Column(Integer, ForeignKey("catalogue.id"), nullable=False)
    added_at = Column(DateTime(timezone=True), server_default=func.now())
    customer = relationship("Customer", back_populates="wishlists")
    product = relationship("Catalogue")
