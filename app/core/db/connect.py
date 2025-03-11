from typing import Generator

from sqlalchemy import Column, DateTime, Engine, create_engine
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker
from sqlalchemy.sql import func

from app.settings.db import DATABASES


def get_database_url(is_test=False):
    db_config = DATABASES["default"]
    engine = db_config["ENGINE"].lower()
    name = db_config["NAME"] if not is_test else "test_db"
    user = db_config.get("USER")
    password = db_config.get("PASSWORD")
    host = db_config.get("HOST", "localhost")
    port = db_config.get("PORT")

    if engine == "mysql":
        return f"mysql+pymysql://{user}:{password}@{host}:{port}/{name}"
    elif engine == "postgresql":
        return f"postgresql://{user}:{password}@{host}:{port}/{name}"
    elif engine == "sqlite":
        return f"sqlite:///{name}.db"
    else:
        raise ValueError(f"Unsupported ENGINE: {engine}")


# สร้างการเชื่อมต่อ
DATABASE_URL = get_database_url()
_engine = create_engine(DATABASE_URL, echo=True)
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=_engine)
Base = declarative_base()


def get_engine() -> Engine:
    return _engine


# Dependency สำหรับ FastAPI
def get_db() -> Generator:
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()


class BaseModel(Base):
    __abstract__ = True
    created_at = Column(DateTime(timezone=True), server_default=func.now())
    updated_at = Column(DateTime(timezone=True), onupdate=func.now())
