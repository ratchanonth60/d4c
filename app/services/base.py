import logging
from contextlib import contextmanager
from typing import Generic, List, Optional, TypeVar

from pydantic import BaseModel as PydanticBaseModel
from sqlalchemy.exc import SQLAlchemyError
from sqlalchemy.orm import Session

from app.core.db.connect import BaseModel
from app.core.exceptions import DatabaseError

ModelType = TypeVar("ModelType", bound=BaseModel)
CreateSchemaType = TypeVar("CreateSchemaType", bound=PydanticBaseModel)
UpdateSchemaType = TypeVar("UpdateSchemaType", bound=PydanticBaseModel)


class BaseService(Generic[ModelType, CreateSchemaType, UpdateSchemaType]):
    """Base service class for common CRUD operations."""

    def __init__(self, model: type[ModelType], db: Session):
        """Initialize the service with a model and database session."""
        self.model = model
        self.db = db
        self.logger = logging.getLogger(__name__)

    @contextmanager
    def _session_scope(self):
        """Provide a transactional scope around a series of operations."""
        try:
            yield self.db
            self.db.commit()
        except SQLAlchemyError as e:
            self.db.rollback()
            raise DatabaseError(f"Database operation failed: {str(e)}")
        finally:
            self.db.close()

    def get(self, id: int) -> Optional[ModelType]:
        """Retrieve an instance by its ID."""
        try:
            with self._session_scope() as session:
                return session.query(self.model).filter(self.model.id == id).first()
        except Exception as e:
            self.logger.error(
                f"Failed to get {self.model.__name__} with id {id}: {str(e)}"
            )
            raise DatabaseError(f"Failed to get {self.model.__name__}: {str(e)}")

    def get_multi(self, skip: int = 0, limit: int = 100) -> List[ModelType]:
        """Retrieve multiple objects with pagination."""
        return self.db.query(self.model).offset(skip).limit(limit).all()

    def create(self, obj_in: CreateSchemaType) -> ModelType:
        """Create a new object."""
        try:
            self.logger.info(f"Creating {self.model.__name__}")
            db_obj = self.model(**obj_in.model_dump())
            with self._session_scope() as session:
                session.add(db_obj)
                session.refresh(db_obj)
            return db_obj
        except SQLAlchemyError as e:
            self.logger.error(f"{self.model.__name__} creation failed: {str(e)}")
            raise DatabaseError(
                f"Failed to create {self.model.__name__.lower()}: {str(e)}"
            )

    def update(self, db_obj: ModelType, obj_in: UpdateSchemaType) -> ModelType:
        """Update an existing object."""
        try:
            update_data = obj_in.model_dump(exclude_unset=True)
            for field, value in update_data.items():
                if hasattr(db_obj, field):
                    setattr(db_obj, field, value)
            with self._session_scope() as session:
                session.add(db_obj)
                session.refresh(db_obj)
            return db_obj
        except SQLAlchemyError as e:
            self.logger.error(f"{self.model.__name__} update failed: {str(e)}")
            raise DatabaseError(
                f"Failed to update {self.model.__name__.lower()}: {str(e)}"
            )

    def remove(self, id: int) -> Optional[ModelType]:
        """Remove an object by ID."""
        try:
            obj = self.db.query(self.model).get(id)
            if not obj:
                self.logger.warning(f"{self.model.__name__} with id {id} not found")
                return None
            with self._session_scope() as session:
                session.delete(obj)
            self.logger.info(f"{self.model.__name__} {id} deleted successfully")
            return obj
        except SQLAlchemyError as e:
            self.logger.error(f"{self.model.__name__} removal failed: {str(e)}")
            raise DatabaseError(
                f"Failed to remove {self.model.__name__.lower()}: {str(e)}"
            )
