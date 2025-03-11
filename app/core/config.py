from fastapi import FastAPI, HTTPException
from fastapi.exceptions import RequestValidationError
from fastapi.middleware.cors import CORSMiddleware

from app import settings
from app.core.auth import JWTMiddleware
from app.core.handlers import (
    authentication_error_handler,
    database_error_handler,
    http_exception_handler,
    validation_exception_handler,
)
from app.core.middleware import log_request_middleware
from .exceptions import AuthenticationError, DatabaseError


def configure_app(app: FastAPI) -> None:
    """Configure basic app settings."""
    app.debug = settings.DEBUG


def configure_middleware(app: FastAPI) -> None:
    """Configure middleware for the application."""
    app.add_middleware(
        CORSMiddleware,
        allow_origins=settings.ALLOW_ORIGINS,
        allow_credentials=True,
        allow_methods=["*"],
        allow_headers=["*"],
    )
    app.add_middleware(JWTMiddleware)
    app.middleware("http")(log_request_middleware)


def configure_exception_handlers(app: FastAPI) -> None:
    """Configure exception handlers for the application."""
    app.exception_handler(RequestValidationError)(validation_exception_handler)
    app.exception_handler(HTTPException)(http_exception_handler)
    app.exception_handler(AuthenticationError)(authentication_error_handler)
    app.exception_handler(DatabaseError)(database_error_handler)
