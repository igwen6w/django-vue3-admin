from typing import Generic, TypeVar, Optional

from pydantic import BaseModel

T = TypeVar("T")

class Response(BaseModel, Generic[T]):
    code: int
    message: str
    data: Optional[T] = None  # ✅ 明确 data 可为 None

def resp_success(data: T, message: str = "success") -> Response[T]:
    return Response(code=0, message=message, data=data)

def resp_error(message="error", code=1) -> Response[None]:
    return Response(code=code, message=message, data=None)