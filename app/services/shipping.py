from sqlalchemy.orm import Session
from app.services.base import BaseService
from app.models.shipping import Shipping
from app.schemas.shipping import ShippingCreate, ShippingUpdate
from app.core.exceptions import DatabaseError


class ShippingService(BaseService[Shipping, ShippingCreate, ShippingUpdate]):
    """Service class for managing shipping-related operations."""

    def __init__(self, db: Session):
        super().__init__(model=Shipping, db=db)

    def create(self, obj_in: ShippingCreate) -> Shipping:
        """Create a new shipping record."""
        try:
            self.logger.info(f"Creating shipping for order_id: {obj_in.order_id}")
            create_data = obj_in.model_dump()
            db_obj = self.model(**create_data)
            with self._session_scope() as session:
                session.add(db_obj)
                session.refresh(db_obj)
            return db_obj
        except Exception as e:
            self.logger.error(f"Shipping creation failed: {str(e)}")
            raise DatabaseError(f"Failed to create shipping: {str(e)}")
