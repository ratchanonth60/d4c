import logging

from fastapi import HTTPException
from fastapi.exceptions import RequestValidationError
from starlette.responses import JSONResponse

from app.core.exceptions import AuthenticationError, DatabaseError
from app.schemas.base import Failed

logger = logging.getLogger(__name__)


async def validation_exception_handler(_, exc: RequestValidationError):
    logger.error(f"Validation error: {exc.errors()}")
    failed = Failed(status="fail", code=422, msg=str(exc.errors()[0]["msg"]))
    return JSONResponse(status_code=422, content=failed.model_dump())


async def http_exception_handler(_, exc: HTTPException):
    logger.error(f"HTTP error: {exc.detail}")
    failed = Failed(status="fail", code=exc.status_code, msg=str(exc.detail))
    return JSONResponse(status_code=exc.status_code, content=failed.model_dump())


async def authentication_error_handler(_, exc: AuthenticationError):
    logger.error(f"Authentication error: {exc.message}")
    failed = Failed(status="fail", code=exc.status_code, msg=exc.message)
    return JSONResponse(status_code=exc.status_code, content=failed.model_dump())


async def database_error_handler(_, exc: DatabaseError):
    logger.error(f"Database error: {exc.message}")
    failed = Failed(status="fail", code=exc.status_code, msg=exc.message)
    return JSONResponse(status_code=exc.status_code, content=failed.model_dump())
