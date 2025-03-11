from sqlalchemy.orm import Session

from app.core.exceptions import DatabaseError
from app.models.catalogue import Catalogue
from app.schemas.catalogue import CatalogueCreate, CatalogueUpdate
from app.services.base import BaseService


class CatalogueService(BaseService[Catalogue, CatalogueCreate, CatalogueUpdate]):
    """Service class for managing catalogue-related operations."""

    def __init__(self, db: Session):
        super().__init__(model=Catalogue, db=db)

    def create(self, obj_in: CatalogueCreate) -> Catalogue:
        """Create a new catalogue item."""
        try:
            self.logger.info(f"Creating catalogue item: {obj_in.name}")
            create_data = obj_in.model_dump()
            db_obj = self.model(**create_data)
            with self._session_scope() as session:
                session.add(db_obj)
                session.refresh(db_obj)
            return db_obj
        except Exception as e:
            self.logger.error(f"Catalogue creation failed: {str(e)}")
            raise DatabaseError(f"Failed to create catalogue: {str(e)}")
