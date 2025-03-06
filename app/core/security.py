from fastapi import Depends
from fastapi.security import OAuth2PasswordBearer
from passlib.context import CryptContext

from .auth_handler import decode_jwt

pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")
oauth2_scheme = OAuth2PasswordBearer(tokenUrl="v1/auth/login")


def get_password_hash(password: str) -> str:
    return pwd_context.hash(password)


async def get_current_user(token: str = Depends(oauth2_scheme)):
    payload = decode_jwt(token)
    return payload.get("id")
