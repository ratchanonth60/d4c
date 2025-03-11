from sqlalchemy.orm import Session
from app.services.base import BaseService
from app.models.wishlist import Wishlist
from app.schemas.wishlist import WishlistCreate, WishlistUpdate
from app.core.exceptions import DatabaseError


class WishlistService(BaseService[Wishlist, WishlistCreate, WishlistUpdate]):
    """Service class for managing wishlist-related operations."""

    def __init__(self, db: Session):
        super().__init__(model=Wishlist, db=db)

    def create(self, obj_in: WishlistCreate) -> Wishlist:
        """Create a new wishlist item."""
        try:
            self.logger.info(
                f"Creating wishlist item for customer_id: {obj_in.customer_id}"
            )
            create_data = obj_in.model_dump()
            db_obj = self.model(**create_data)
            with self._session_scope() as session:
                session.add(db_obj)
                session.refresh(db_obj)
            return db_obj
        except Exception as e:
            self.logger.error(f"Wishlist creation failed: {str(e)}")
            raise DatabaseError(f"Failed to create wishlist: {str(e)}")
