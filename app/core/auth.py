from fastapi import Request
from fastapi.security.utils import get_authorization_scheme_param
from starlette.middleware.base import BaseHTTPMiddleware

from app.core.auth_handler import decode_jwt
from app.core.db.connect import SessionLocal
from app.core.exceptions import AuthenticationError
from app.models.user import User


class JWTMiddleware(BaseHTTPMiddleware):
    """Middleware to authenticate requests using JWT and attach user to request state."""

    async def dispatch(self, request: Request, call_next):
        """Process the request and attach authenticated user to request.state."""
        request.state.user = None  # Default to no user

        auth_header = request.headers.get("Authorization")
        if auth_header:
            scheme, token = get_authorization_scheme_param(auth_header)
            if scheme.lower() == "bearer":
                with SessionLocal() as db:
                    try:
                        payload = decode_jwt(token)
                        if not payload:
                            raise AuthenticationError("Invalid token", status_code=401)

                        username = payload.get("sub")
                        if not username:
                            raise AuthenticationError(
                                "Invalid token payload", status_code=401
                            )

                        user = db.query(User).filter(User.username == username).first()
                        if not user:
                            raise AuthenticationError("User not found", status_code=403)

                        request.state.user = user
                    except AuthenticationError as e:
                        raise e

        response = await call_next(request)
        return response
