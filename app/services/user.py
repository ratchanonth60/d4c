import logging
from typing import Optional

from sqlalchemy.exc import SQLAlchemyError
from sqlalchemy.orm import Session

from app.core.security import get_password_hash
from app.models.user import User
from app.schemas.user import UserCreate, UserUpdate

from .base import BaseService


class UserService(BaseService[User, UserCreate, UserUpdate]):
    def __init__(self, db: Session):
        super().__init__(User, db)
        self.logger = logging.getLogger(__name__)

    def get_by_email(self, email: str) -> Optional[User]:
        return self.db.query(User).filter(User.email == email).first()

    def create(self, obj_in: UserCreate) -> User:
        try:
            obj_in.validate(obj_in)
            create_data = obj_in.model_dump()
            create_data["hashed_password"] = get_password_hash(
                create_data.pop("password")
            )
            db_obj = self.model(**create_data)
            with self._session_scope() as session:
                session.add(db_obj)
                session.commit()
                session.refresh(db_obj)
            return db_obj
        except SQLAlchemyError as e:
            self.logger.error(f"Error creating user: {str(e)}")
            raise e

    def update(self, db_obj: User, obj_in: UserUpdate) -> User:
        try:
            update_data = obj_in.model_dump(exclude_unset=True)
            if "password" in update_data:
                update_data["hashed_password"] = get_password_hash(
                    update_data.pop("password")
                )
            for field, value in update_data.items():
                if hasattr(db_obj, field):
                    setattr(db_obj, field, value)
            with self._session_scope() as session:
                session.add(db_obj)
                session.commit()
                session.refresh(db_obj)
            return db_obj
        except SQLAlchemyError as e:
            self.logger.error(f"Error updating user: {str(e)}")
            raise e
