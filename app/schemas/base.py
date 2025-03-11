from typing import Any, Generic, TypeVar

from pydantic import BaseModel

T = TypeVar("T")


class BaseResponse(BaseModel):
    status: str
    code: int
    msg: str


class Successfully(BaseResponse, Generic[T]):
    status: str = "success"
    data: Any = None


class Failed(BaseResponse):
    status: str = "fail"
