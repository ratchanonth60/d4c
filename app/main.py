import logging

from fastapi import FastAPI
from fastapi.security import OAuth2AuthorizationCodeBearer
from app.api.v1.address import router as address_router
from app.api.v1.auth import router as auth_router
from app.api.v1.cart import router as cart_router
from app.api.v1.users import router as users_router
from app.api.v1.catalogue import router as catalogue_router
from app.api.v1.checkout import router as checkout_router
from app.core.config import (
    configure_app,
    configure_exception_handlers,
    configure_middleware,
)
from app.core.db.connect import Base, get_engine

logger = logging.getLogger(__name__)
oauth2_scheme = OAuth2AuthorizationCodeBearer(
    authorizationUrl="/v1/auth/login",  # URL สำหรับการขอ token (ในที่นี้เป็น placeholder)
    tokenUrl="/v1/auth/login",  # URL สำหรับการขอ token (ในที่นี้เป็น placeholder)
)


def create_app(db_engine=None) -> FastAPI:
    """Factory function to create and configure the FastAPI app."""
    app = FastAPI(
        title="E-commerce API",
        description="API for an e-commerce platform",
        version="1.0.0",
    )
    engine = db_engine if db_engine is not None else get_engine()

    @app.on_event("startup")
    async def startup_event():
        Base.metadata.create_all(bind=engine)
        logger.info("Application started and database initialized")

    @app.on_event("shutdown")
    async def shutdown_event():
        logger.info("Application shutting down")

    configure_app(app)
    configure_middleware(app)
    configure_exception_handlers(app)
    app.include_router(auth_router, prefix="/v1")
    app.include_router(users_router, prefix="/v1")
    app.include_router(address_router, prefix="/v1")
    app.include_router(cart_router, prefix="/v1")
    app.include_router(catalogue_router, prefix="/v1")
    app.include_router(checkout_router, prefix="/v1")

    @app.get("/")
    def read_root():
        return {"message": "Welcome to E-commerce API"}

    return app


app = create_app()
