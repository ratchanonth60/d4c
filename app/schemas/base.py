from pydantic import BaseModel
from typing import Generic, TypeVar, Optional, Any

T = TypeVar("T")


class BaseResponse(BaseModel, Generic[T]):
    status: str
    code: int
    msg: Optional[T] = None


class Successfully(BaseResponse):
    data: Any = None


class Failed(BaseResponse):
    pass
