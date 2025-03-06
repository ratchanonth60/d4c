from fastapi import Request, Response
from fastapi.security.utils import get_authorization_scheme_param
from sqlalchemy.orm import Session
from starlette.middleware.base import BaseHTTPMiddleware
from starlette.responses import JSONResponse

from app.core.db.connect import SessionLocal
from app.models.user import User

from .auth_handler import decode_jwt


class JWTMiddleware(BaseHTTPMiddleware):
    async def dispatch(self, request: Request, call_next) -> Response:
        request.state.user = None  # ตั้งค่าเริ่มต้นให้ user เป็น None

        auth_header = request.headers.get("Authorization")
        if auth_header:
            scheme, token = get_authorization_scheme_param(auth_header)
            if scheme.lower() == "bearer":
                payload = decode_jwt(token)
                if payload:
                    db: Session = SessionLocal()
                    user = (
                        db.query(User)
                        .filter(User.username == payload.get("sub"))
                        .first()
                    )
                    db.close()

                    if user:
                        request.state.user = user
                    else:
                        return JSONResponse(
                            status_code=403, content={"detail": "User not found"}
                        )

        response = await call_next(request)
        return response
