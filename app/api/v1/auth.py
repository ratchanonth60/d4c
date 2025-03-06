from fastapi import APIRouter, Depends
import jwt
from sqlalchemy.orm import Session
from fastapi.security import OAuth2PasswordRequestForm


from app.core.auth_handler import sign_jwt, sign_refresh_token, decode_jwt
from app.core.db.connect import get_db
from app.core.security import get_password_hash
from app.models.user import User
from app.schemas.auth import (
    JWTBearer,
    UserCreate,
    UserResponse,
    RefreshTokenRequest,
)
from app.schemas.base import Failed, Successfully

router = APIRouter(prefix="/auth", tags=["auth"])


@router.post("/login")
def login(
    form_data: OAuth2PasswordRequestForm = Depends(),
    db: Session = Depends(get_db),
):
    user = db.query(User).filter(User.username == form_data.username).first()
    print(user)
    if not user or not user.verify_password(form_data.password):
        return Failed(status="fail", code=404, msg="Invalid username or password")
    user.update_last_login()
    db.commit()
    id = str(user.id)
    access_token, refresh_token = sign_jwt(id), sign_refresh_token(id)
    jwt_token = JWTBearer(
        access_token=access_token, refresh_token=refresh_token, token_type="bearer"
    )
    return Successfully(
        code=200, msg="Login successfully", data=jwt_token, status="success"
    )


@router.post("/register", response_model=UserResponse)
async def register(user: UserCreate, db: Session = Depends(get_db)):
    existing_user = (
        db.query(User)
        .filter((User.username == user.username) | (User.email == user.email))
        .first()
    )

    if existing_user:
        return Failed(status="fail", code=400, msg="Username or email already exists")
    hashed_password = get_password_hash(user.password)

    new_user = User(
        username=user.username, email=user.email, hashed_password=hashed_password
    )

    db.add(new_user)
    db.commit()
    db.refresh(new_user)

    return Successfully(status="fail", code=201, msg="User created", data=user)


@router.post("/refresh")
def refresh_token(refresh_token_request: RefreshTokenRequest):
    try:
        payload = decode_jwt(refresh_token_request.refresh_token)
        user_id = payload.get("id")
        if not user_id:
            return Failed(status="fail", code=401, msg="Invalid refresh token")
        new_access_token = sign_jwt(user_id)

        return Successfully(
            status="success", code=200, msg="Refresh token", data=new_access_token
        )
    except jwt.ExpiredSignatureError:
        return Failed(status="fail", code=401, msg="Refresh token is expired")
    except jwt.PyJWKError:
        return Failed(status="fail", code=401, msg="Invalid refresh token")
