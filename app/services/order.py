from sqlalchemy.orm import Session

from app.core.exceptions import DatabaseError
from app.models.order import Order
from app.schemas.order import OrderCreate, OrderUpdate
from app.services.base import BaseService


class OrderService(BaseService[Order, OrderCreate, OrderUpdate]):
    """Service class for managing order-related operations."""

    def __init__(self, db: Session):
        super().__init__(model=Order, db=db)

    def create(self, obj_in: OrderCreate) -> Order:
        """Create a new order."""
        try:
            self.logger.info(f"Creating order for customer_id: {obj_in.customer_id}")
            create_data = obj_in.model_dump()
            db_obj = self.model(**create_data)
            with self._session_scope() as session:
                session.add(db_obj)
                session.refresh(db_obj)
            return db_obj
        except Exception as e:
            self.logger.error(f"Order creation failed: {str(e)}")
            raise DatabaseError(f"Failed to create order: {str(e)}")
