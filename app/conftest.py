from typing import Generator

import pytest
from fastapi.testclient import TestClient
from sqlalchemy import create_engine, text
from sqlalchemy.exc import ProgrammingError
from sqlalchemy.orm import Session, session, sessionmaker

from app.core.db.connect import Base, get_database_url, get_db
from app.factory.address import AddressFactory
from app.factory.user import UserFactory
from app.main import app

TEST_SQLALCHEMY_DATABASE_URL = get_database_url(True)
admin_engine = create_engine(get_database_url(True), isolation_level="AUTOCOMMIT")

# Create an engine and sessionmaker bound to the test database
engine = create_engine(TEST_SQLALCHEMY_DATABASE_URL)
TestingSessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)


def create_test_database():
    """Create the test database if it doesn't exist."""
    with admin_engine.connect() as connection:
        try:
            connection.execute(
                text(f"CREATE DATABASE {TEST_SQLALCHEMY_DATABASE_URL.split('/')[-1]}")
            )
        except ProgrammingError:
            print("Database already exists, continuing...")


@pytest.fixture(scope="session", autouse=True)
def setup_test_database():
    """
    Create the test database schema before any tests run,
    and drop it after all tests are done.
    """
    create_test_database()  # Ensure the test database is created
    Base.metadata.create_all(bind=engine)  # Create tables
    yield
    Base.metadata.drop_all(bind=engine)  # Drop tables after tests


@pytest.fixture(scope="function")
def db() -> Generator:
    """
    Create a new database session for each test and roll it back after the test.
    """
    connection = engine.connect()
    transaction = connection.begin()
    session = TestingSessionLocal(bind=connection)

    yield session

    session.close()
    transaction.rollback()
    connection.close()


@pytest.fixture(scope="function")
def client(db: session) -> Generator[TestClient, None, None]:
    """
    Provide a TestClient that uses the test database session.
    Override the get_db dependency to use the test session.
    """

    def override_get_db():
        yield db

    app.dependency_overrides[get_db] = override_get_db
    with TestClient(app) as c:
        yield c
    app.dependency_overrides.clear()


@pytest.fixture(autouse=True)
def set_session_for_factories(db: Session):
    UserFactory._meta.sqlalchemy_session = db
    AddressFactory._meta.sqlalchemy_session = db
