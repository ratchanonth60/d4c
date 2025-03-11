import enum

from passlib.context import CryptContext
from sqlalchemy import Boolean, Column, DateTime, Enum, Integer, String
from sqlalchemy.orm import relationship
from sqlalchemy.sql import func

from app.core.db.connect import BaseModel

pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")


class UserRole(str, enum.Enum):
    USER = "user"
    ADMIN = "admin"


class User(BaseModel):
    __tablename__ = "users"

    # Primary key
    id = Column(Integer, primary_key=True, index=True)

    # ข้อมูลบัญชี
    username = Column(String, unique=True, index=True, nullable=False)
    email = Column(String, unique=True, index=True, nullable=False)
    hashed_password = Column(String, nullable=False)  # รหัสผ่านที่เข้ารหัส
    role = Column(Enum(UserRole), default=UserRole.USER, nullable=False)
    is_active = Column(Boolean, default=True)  # บัญชีเปิดใช้งานหรือไม่
    is_verified = Column(Boolean, default=False)  # อีเมลยืนยันแล้วหรือไม่

    last_login = Column(DateTime(timezone=True), nullable=True)

    addresses = relationship("Address", back_populates="user")

    # # ความสัมพันธ์กับตารางอื่น
    # orders = relationship("Order", back_populates="user")  # ความสัมพันธ์กับคำสั่งซื้อ
    # cart_items = relationship("Cart", back_populates="user")  # ความสัมพันธ์กับตะกร้าสินค้า
    #
    def __repr__(self):
        return f"<User(id={self.id}, username={self.username}, email={self.email})>"

    def verify_password(self, plain_password: str) -> bool:
        return pwd_context.verify(plain_password, str(self.hashed_password))

    # Method สำหรับอัปเดต last_login
    def update_last_login(self):
        self.last_login = func.now()

    # Method สำหรับแปลงข้อมูลเป็น dictionary
    def to_dict(self) -> dict:
        return {
            "id": self.id,
            "username": self.username,
            "email": self.email,
            "last_login": self.last_login.isoformat() if self.last_login else None,
            "created_at": self.created_at.isoformat(),
            "updated_at": self.updated_at.isoformat() if self.updated_at else None,
        }
