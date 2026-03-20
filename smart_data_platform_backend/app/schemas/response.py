from pydantic import BaseModel
from typing import Optional, Any


class BaseResponse(BaseModel):
    """
    基础响应结构
    """
    success: bool
    message: str
    data: Optional[Any] = None
    error_code: Optional[str] = None