from sqlalchemy.orm import Session

from app.core.exceptions import DatabaseError
from app.models.offer import Offer, Voucher
from app.schemas.offer import OfferCreate, OfferUpdate, VoucherCreate, VoucherUpdate
from app.services.base import BaseService


class OfferService(BaseService[Offer, OfferCreate, OfferUpdate]):
    """Service class for managing offer-related operations."""

    def __init__(self, db: Session):
        super().__init__(model=Offer, db=db)

    def create(self, obj_in: OfferCreate) -> Offer:
        """Create a new offer."""
        try:
            self.logger.info(f"Creating offer: {obj_in.name}")
            create_data = obj_in.model_dump()
            db_obj = self.model(**create_data)
            with self._session_scope() as session:
                session.add(db_obj)
                session.refresh(db_obj)
            return db_obj
        except Exception as e:
            self.logger.error(f"Offer creation failed: {str(e)}")
            raise DatabaseError(f"Failed to create offer: {str(e)}")


class VoucherService(BaseService[Voucher, VoucherCreate, VoucherUpdate]):
    """Service class for managing voucher-related operations."""

    def __init__(self, db: Session):
        super().__init__(model=Voucher, db=db)

    def create(self, obj_in: VoucherCreate) -> Voucher:
        """Create a new voucher."""
        try:
            self.logger.info(f"Creating voucher: {obj_in.code}")
            create_data = obj_in.model_dump()
            db_obj = self.model(**create_data)
            with self._session_scope() as session:
                session.add(db_obj)
                session.refresh(db_obj)
            return db_obj
        except Exception as e:
            self.logger.error(f"Voucher creation failed: {str(e)}")
            raise DatabaseError(f"Failed to create voucher: {str(e)}")
