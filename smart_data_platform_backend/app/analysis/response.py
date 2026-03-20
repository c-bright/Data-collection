"""
统一响应工具类 - FastAPI版本
提供标准化的API响应格式
"""

from typing import Any, Optional, Dict, Union
from pydantic import BaseModel


class Result:
    """
    统一响应工具类，封装API响应标准
    
    使用示例:
        # 成功响应
        return Result.success(data={"users": []}, msg="获取成功")
        
        # 错误响应  
        return Result.error(msg="用户不存在", error_code="USER_NOT_FOUND")
    """
    
    @staticmethod
    def success(data: Any = None, msg: str = "操作成功") -> Dict[str, Any]:
        """
        成功响应
        
        Args:
            data: 返回的数据
            msg: 成功消息
            
        Returns:
            标准化响应字典
        """
        return {
            "success": True,
            "message": msg,
            "data": data,
            "error_code": None
        }
    
    @staticmethod
    def error(msg: str = "操作失败", error_code: Optional[str] = "UNKNOWN_ERROR") -> Dict[str, Any]:
        """
        错误响应
        
        Args:
            msg: 错误消息
            error_code: 错误代码
            
        Returns:
            标准化响应字典
        """
        return {
            "success": False,
            "message": msg,
            "data": None,
            "error_code": error_code
        }
    
    @staticmethod
    def paginate(data: list, total: int, page: int, size: int, msg: str = "获取成功") -> Dict[str, Any]:
        """
        分页响应
        
        Args:
            data: 当前页数据列表
            total: 总记录数
            page: 当前页码
            size: 每页大小
            msg: 成功消息
            
        Returns:
            标准化分页响应字典
        """
        return Result.success({
            "items": data,
            "total": total,
            "page": page,
            "size": size
        }, msg)


class PaginatedResponse(BaseModel):
    """
    分页响应数据模型
    """
    items: list
    total: int
    page: int
    size: int


# 更新analysis模块的__init__.py
"""
from .response import Result, PaginatedResponse

__all__ = ['Result', 'PaginatedResponse', 'ProductStatsAnalyzer', 'CommentAnalyzer', 'TagAnalyzer']
"""
