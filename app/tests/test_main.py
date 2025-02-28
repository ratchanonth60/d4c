import sys
import os
import pytest
from fastapi.testclient import TestClient
from sqlmodel import Session, select
from app.main import app, engine, SQLModel, Hero  # อัปเดต import

# เพิ่ม path ของ app ลงใน sys.path
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), "..")))

client = TestClient(app)


@pytest.fixture(scope="session", autouse=True)
async def setup_db():
    # ใช้ engine จาก SQLModel แทน
    SQLModel.metadata.create_all(engine)
    yield
    # ไม่ต้อง disconnect เพราะใช้ Session กับ engine


def test_read_root():
    response = client.post(
        "/heroes/",
        json={"name": "Spider-Man", "secret_name": "Peter Parker", "age": 25},
    )
    assert response.status_code == 200
    assert "id" in response.json()

    response = client.get("/heroes/")
    assert response.status_code == 200
    assert len(response.json()) > 0


@pytest.mark.asyncio
async def test_db_connection():
    with Session(engine) as session:
        hero = Hero(name="Batman", secret_name="Bruce Wayne", age=35)
        session.add(hero)
        session.commit()
        session.refresh(hero)

        query = select(Hero).where(Hero.name == "Batman")
        result = session.exec(query).first()
        assert result is not None
        assert result.name == "Batman"
