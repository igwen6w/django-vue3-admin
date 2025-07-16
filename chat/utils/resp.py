from typing import Any, Optional
from pydantic import BaseModel

class CommonResponse(BaseModel):
    code: int = 0
    message: str = "success"
    data: Any = None
    error: Optional[Any] = None


def resp_success(data=None, message="success"):
    return CommonResponse(code=0, message=message, data=data, error=None)


def resp_error(message="error", code=1, error=None):
    return CommonResponse(code=code, message=message, data=None, error=error)