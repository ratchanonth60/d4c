from datetime import datetime
from typing import Optional

from pydantic import BaseModel, EmailStr, Field, validator

from app.models.user import UserRole


# Schema พื้นฐาน
class UserBase(BaseModel):
    username: str = Field(..., min_length=3, max_length=50)
    email: EmailStr


# Schema สำหรับสร้างผู้ใช้ใหม่
class UserCreate(UserBase):
    password: str = Field(..., min_length=8)
    first_name: Optional[str] = None
    last_name: Optional[str] = None
    phone_number: Optional[str] = None

    @validator("password")
    def password_strength(cls, v):
        if not any(c.isupper() for c in v) or not any(c.isdigit() for c in v):
            raise ValueError(
                "Password must contain at least one uppercase letter and one number"
            )
        return v


# Schema สำหรับอัปเดตข้อมูลผู้ใช้
class UserUpdate(BaseModel):
    first_name: Optional[str] = None
    last_name: Optional[str] = None
    phone_number: Optional[str] = None
    address_line1: Optional[str] = None
    address_line2: Optional[str] = None
    city: Optional[str] = None
    state: Optional[str] = None
    postal_code: Optional[str] = None
    country: Optional[str] = None


# Schema สำหรับแสดงข้อมูลผู้ใช้
class User(UserBase):
    id: int
    first_name: Optional[str]
    last_name: Optional[str]
    phone_number: Optional[str]
    address_line1: Optional[str]
    address_line2: Optional[str]
    city: Optional[str]
    state: Optional[str]
    postal_code: Optional[str]
    country: Optional[str]
    role: UserRole
    is_active: bool
    is_verified: bool
    created_at: datetime
    updated_at: Optional[datetime]
    last_login: Optional[datetime]

    class Config:
        orm_mode = True  # อนุญาตให้แปลงจาก SQLAlchemy object
