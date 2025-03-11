from datetime import datetime, timedelta
from typing import Optional

import jwt
from sqlalchemy.exc import SQLAlchemyError
from sqlalchemy.orm import Session

from app import settings
from app.core.auth_handler import decode_jwt, sign_jwt, sign_refresh_token
from app.core.exceptions import AuthenticationError, DatabaseError
from app.core.security import get_password_hash
from app.models.user import User
from app.schemas.auth import (
    ConfirmPasswordRequest,
    JWTBearer,
    RefreshTokenRequest,
    ResetPasswordRequest,
    UserCreate,
    UserResponse,
)
from app.services.base import BaseService
from app.services.email import EmailService


class AuthService(BaseService[User, UserCreate, UserResponse]):
    """Service class for authentication-related operations."""

    def __init__(self, db: Session, email_service: Optional[EmailService] = None):
        """Initialize the auth service."""
        super().__init__(model=User, db=db)
        self.email_service = email_service or EmailService()

    def login(self, username: str, password: str) -> JWTBearer:
        """Authenticate a user and return JWT tokens."""
        try:
            user = self.db.query(User).filter(User.username == username).first()
            if not user or not user.verify_password(password):
                raise AuthenticationError(
                    "Invalid username or password", status_code=404
                )
            if not user.is_active:
                raise AuthenticationError("User is not active", status_code=401)

            user.update_last_login()
            self.db.commit()

            user_id = str(user.id)
            access_token = sign_jwt(user_id)
            refresh_token = sign_refresh_token(user_id)
            return JWTBearer(
                access_token=access_token,
                refresh_token=refresh_token,
                token_type="bearer",
            )
        except SQLAlchemyError as e:
            self.logger.error(f"Login failed: {str(e)}")
            raise DatabaseError(f"Failed to process login: {str(e)}")

    def register(self, obj_in: UserCreate, background_tasks) -> UserResponse:
        """Register a new user and send a welcome email."""
        try:
            existing_user = (
                self.db.query(User)
                .filter(
                    (User.username == obj_in.username) | (User.email == obj_in.email)
                )
                .first()
            )
            if existing_user:
                raise AuthenticationError(
                    "Username or email already exists", status_code=400
                )

            create_data = obj_in.model_dump()
            create_data["hashed_password"] = get_password_hash(
                create_data.pop("password")
            )
            new_user = User(**create_data)

            with self._session_scope() as session:
                session.add(new_user)
                session.refresh(new_user)

            self.email_service.send_template_email(
                background_tasks=background_tasks,
                to_emails=new_user.email,
                template_name="welcome.html",
                subject=f"Welcome to {settings.PROJECT_NAME}",
                template_data={
                    "app_name": settings.PROJECT_NAME,
                    "username": new_user.username or new_user.email.split("@")[0],
                    "current_year": datetime.now().year,
                    "plain_text": f"Welcome to {settings.PROJECT_NAME}! Thank you for joining us.",
                },
            )

            return UserResponse.from_orm(new_user)
        except SQLAlchemyError as e:
            self.logger.error(f"Registration failed: {str(e)}")
            raise DatabaseError(f"Failed to register user: {str(e)}")

    def refresh_token(self, refresh_token: RefreshTokenRequest) -> str:
        """Refresh an access token using a refresh token."""
        try:
            payload = decode_jwt(refresh_token.refresh_token)
            user_id = payload.get("id")
            if not user_id:
                raise AuthenticationError("Invalid refresh token", status_code=401)

            return sign_jwt(user_id)
        except jwt.ExpiredSignatureError:
            raise AuthenticationError("Refresh token is expired", status_code=401)
        except jwt.PyJWKError:
            raise AuthenticationError("Invalid refresh token", status_code=401)

    def reset_password_request(self, email: str) -> str:
        """Request a password reset token."""
        try:
            user = self.db.query(User).filter(User.email == email).first()
            if not user:
                raise AuthenticationError("Email not found", status_code=404)

            return sign_jwt(str(user.id), exp=timedelta(minutes=5))
        except SQLAlchemyError as e:
            self.logger.error(f"Reset password request failed: {str(e)}")
            raise DatabaseError(f"Failed to process reset password request: {str(e)}")

    def reset_password(self, request: ResetPasswordRequest) -> None:
        """Reset a user's password using a reset token."""
        try:
            payload = decode_jwt(request.token)
            user_id = payload.get("id")
            if not user_id:
                raise AuthenticationError("Invalid token", status_code=401)

            user = self.db.query(User).filter(User.id == user_id).first()
            if not user:
                raise AuthenticationError("User not found", status_code=404)

            user.hashed_password = get_password_hash(request.new_password)
            user.update_last_login()
            with self._session_scope() as session:
                session.add(user)
        except jwt.ExpiredSignatureError:
            raise AuthenticationError("Token expired", status_code=401)
        except jwt.PyJWKError:
            raise AuthenticationError("Invalid token", status_code=401)
        except SQLAlchemyError as e:
            self.logger.error(f"Password reset failed: {str(e)}")
            raise DatabaseError(f"Failed to reset password: {str(e)}")

    def confirm_password(self, request: ConfirmPasswordRequest) -> None:
        """Confirm and update a user's password."""
        try:
            user = self.db.query(User).filter(User.username == request.username).first()
            if not user or not user.verify_password(request.old_password):
                raise AuthenticationError(
                    "Invalid username or password", status_code=400
                )

            user.hashed_password = get_password_hash(request.new_password)
            user.update_last_login()
            with self._session_scope() as session:
                session.add(user)
        except SQLAlchemyError as e:
            self.logger.error(f"Password confirmation failed: {str(e)}")
            raise DatabaseError(f"Failed to update password: {str(e)}")
