from sqlalchemy.orm import Session

from app.core.exceptions import DatabaseError
from app.models.address import Address
from app.schemas.address import AddressCreate, AddressUpdate
from app.services.base import BaseService


class AddressService(BaseService[Address, AddressCreate, AddressUpdate]):
    """Service class for managing address-related operations."""

    def __init__(self, db: Session):
        """Initialize the address service."""
        super().__init__(model=Address, db=db)

    def create(self, obj_in: AddressCreate) -> Address:
        """Create a new address for a specific user."""
        try:
            self.logger.info(f"Creating address for user_id: {obj_in.user_id}")
            create_data = obj_in.model_dump()
            create_data["user_id"] = obj_in.user_id
            db_obj = self.model(**create_data)
            with self._session_scope() as session:
                session.add(db_obj)
                session.refresh(db_obj)
            return db_obj
        except Exception as e:
            self.logger.error(f"Address creation failed: {str(e)}")
            raise DatabaseError(f"Failed to create address: {str(e)}")
