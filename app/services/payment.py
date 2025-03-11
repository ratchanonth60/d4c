from sqlalchemy.orm import Session

from app.core.exceptions import DatabaseError
from app.models.payment import Payment
from app.schemas.payment import PaymentCreate, PaymentUpdate
from app.services.base import BaseService


class PaymentService(BaseService[Payment, PaymentCreate, PaymentUpdate]):
    """Service class for managing payment-related operations."""

    def __init__(self, db: Session):
        super().__init__(model=Payment, db=db)

    def create(self, obj_in: PaymentCreate) -> Payment:
        """Create a new payment."""
        try:
            self.logger.info(f"Creating payment for order_id: {obj_in.order_id}")
            create_data = obj_in.model_dump()
            db_obj = self.model(**create_data)
            with self._session_scope() as session:
                session.add(db_obj)
                session.refresh(db_obj)
            return db_obj
        except Exception as e:
            self.logger.error(f"Payment creation failed: {str(e)}")
            raise DatabaseError(f"Failed to create payment: {str(e)}")
