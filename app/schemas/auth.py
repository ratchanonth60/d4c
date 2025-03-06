from pydantic import BaseModel, EmailStr


class JWTBearer(BaseModel):
    access_token: str
    refresh_token: str
    token_type: str


class RefreshTokenRequest(BaseModel):
    refresh_token: str


class UserLogin(BaseModel):
    username: str
    password: str

    class Config:
        json_schema_extra = {
            "example": {"username": "abdulazeez@x.com", "password": "weakpassword"}
        }


class UserCreate(BaseModel):
    username: str
    email: EmailStr
    password: str
    password_confirm: str


class UserResponse(BaseModel):
    id: int
    username: str
    email: EmailStr
    is_active: bool

    class Config:
        orm_mode = True
