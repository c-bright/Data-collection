
from pydantic import BaseModel
from typing import Optional
from datetime import datetime

class ProductRequest(BaseModel):
    """
    商品查询请求结构
    """
    keyword: str
    page: int = 1
    page_size: int = 20

class ProductResponse(BaseModel):
    """
    商品数据响应结构
    """
    id: str
    name: str
    price: float
    link: Optional[str] = None
    image_url: Optional[str] = None
    shop_name: Optional[str] = None
    category: Optional[str] = None
    rating: Optional[float] = None
    comment_count: Optional[int] = None
    created_at: Optional[datetime] = None

class ProductListResponse(BaseModel):
    """
    商品列表响应结构
    """
    products: list[ProductResponse]
    total: int
    page: int
    page_size: int