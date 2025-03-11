from sqlalchemy.orm import Session

from app.core.exceptions import DatabaseError
from app.models.checkout import Checkout
from app.schemas.checkout import CheckoutCreate, CheckoutUpdate
from app.services.base import BaseService


class CheckoutService(BaseService[Checkout, CheckoutCreate, CheckoutUpdate]):
    """Service class for managing checkout-related operations."""

    def __init__(self, db: Session):
        super().__init__(model=Checkout, db=db)

    def create(self, obj_in: CheckoutCreate) -> Checkout:
        """Create a new checkout session."""
        try:
            self.logger.info(f"Creating checkout for order_id: {obj_in.order_id}")
            create_data = obj_in.model_dump()
            db_obj = self.model(**create_data)
            with self._session_scope() as session:
                session.add(db_obj)
                session.refresh(db_obj)
            return db_obj
        except Exception as e:
            self.logger.error(f"Checkout creation failed: {str(e)}")
            raise DatabaseError(f"Failed to create checkout: {str(e)}")
