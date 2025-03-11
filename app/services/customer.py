from sqlalchemy.orm import Session
from passlib.context import CryptContext
from app.services.base import BaseService
from app.models.customer import Customer
from app.schemas.customer import CustomerCreate, CustomerUpdate
from app.core.exceptions import DatabaseError

pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")


class CustomerService(BaseService[Customer, CustomerCreate, CustomerUpdate]):
    """Service class for managing customer-related operations."""

    def __init__(self, db: Session):
        super().__init__(model=Customer, db=db)

    def create(self, obj_in: CustomerCreate) -> Customer:
        """Create a new customer."""
        try:
            self.logger.info(f"Creating customer: {obj_in.username}")
            create_data = obj_in.model_dump()
            create_data["hashed_password"] = pwd_context.hash(obj_in.password)
            del create_data["password"]
            db_obj = self.model(**create_data)
            with self._session_scope() as session:
                session.add(db_obj)
                session.refresh(db_obj)
            return db_obj
        except Exception as e:
            self.logger.error(f"Customer creation failed: {str(e)}")
            raise DatabaseError(f"Failed to create customer: {str(e)}")
