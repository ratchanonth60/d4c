from sqlalchemy import Column, DateTime, create_engine
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker
from sqlalchemy.sql import func

from app.settings.db import DATABASES


def get_database_url():
    db_config = DATABASES["default"]
    engine = db_config["ENGINE"].lower()
    name = db_config["NAME"]
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
print(DATABASE_URL)
engine = create_engine(DATABASE_URL, echo=True)
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)
Base = declarative_base()


# Dependency สำหรับ FastAPI
def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()


class BaseModel(Base):
    __abstract__ = True
    created_at = Column(DateTime(timezone=True), server_default=func.now())
    updated_at = Column(DateTime(timezone=True), onupdate=func.now())
