from fastapi import FastAPI, HTTPException
from fastapi.exceptions import RequestValidationError
from fastapi.middleware.cors import CORSMiddleware

from app.schemas.base import Failed

from .api.v1 import auth
from .core.auth import JWTMiddleware
from .core.db.connect import Base, engine
from .core.middleware import log_request_middleware
from .settings.base import ALLOW_ORIGINS

Base.metadata.create_all(bind=engine)


app = FastAPI()

app.include_router(auth.router, prefix="/v1")
app.middleware("http")(log_request_middleware)

app.add_middleware(JWTMiddleware)
app.add_middleware(
    CORSMiddleware,
    allow_origins=ALLOW_ORIGINS,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


@app.exception_handler(RequestValidationError)
async def validation_exception_handler(_, exc):
    return Failed(status="fail", code=exc.status_code, msg=str(exc.errors()[0]["msg"]))


@app.exception_handler(HTTPException)
async def http_exception_handler(_, exc):
    return Failed(status="fail", code=exc.status_code, msg=str(exc.detail))


@app.get("/")
def read_root():
    return {"message": "Welcome to E-commerce API"}
