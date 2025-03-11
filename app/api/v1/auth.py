from fastapi import APIRouter, BackgroundTasks, Depends
from fastapi.security import OAuth2PasswordRequestForm
from sqlalchemy.orm import Session

from app.core.db.connect import get_db
from app.schemas.auth import (
    ConfirmPasswordRequest,
    RefreshTokenRequest,
    ResetPasswordRequest,
    UserCreate,
)
from app.schemas.base import Successfully
from app.services.auth import AuthService

router = APIRouter(prefix="/auth", tags=["auth"])


def get_auth_service(db: Session = Depends(get_db)) -> AuthService:
    return AuthService(db)


@router.post("/login")
def login(
    form_data: OAuth2PasswordRequestForm = Depends(),
    auth_service: AuthService = Depends(get_auth_service),
):
    jwt_token = auth_service.login(form_data.username, form_data.password)
    return Successfully(
        code=200, msg="Login successfully", data=jwt_token, status="success"
    )


@router.post("/register")
async def register(
    user: UserCreate,
    background_tasks: BackgroundTasks,
    auth_service: AuthService = Depends(get_auth_service),
):
    new_user = auth_service.register(user, background_tasks)
    return Successfully(status="success", code=201, msg="User created", data=new_user)


@router.post("/refresh")
def refresh_token(
    refresh_token_request: RefreshTokenRequest,
    auth_service: AuthService = Depends(get_auth_service),
):
    new_access_token = auth_service.refresh_token(refresh_token_request)
    return Successfully(
        status="success", code=200, msg="Refresh token", data=new_access_token
    )


@router.post("/reset-password-request")
def reset_password_request(
    email: str,
    auth_service: AuthService = Depends(get_auth_service),
):
    reset_token = auth_service.reset_password_request(email)
    return Successfully(
        code=200,
        msg="Reset password token sent",
        data=reset_token,
        status="success",
    )


@router.post("/reset-password")
def reset_password(
    request: ResetPasswordRequest,
    auth_service: AuthService = Depends(get_auth_service),
):
    auth_service.reset_password(request)
    return Successfully(code=200, msg="Password reset successfully", status="success")


@router.post("/confirm-password")
def confirm_password(
    request: ConfirmPasswordRequest,
    auth_service: AuthService = Depends(get_auth_service),
):
    auth_service.confirm_password(request)
    return Successfully(code=200, msg="Password updated successfully", status="success")
