from sqlalchemy import Column, Integer, String
from app.models.product_model import Base # 确保使用相同的 Base 以便管理

class User(Base):
    """
    用户数据模型，用于处理用户注册与登录
    """
    __tablename__ = 'user'

    id = Column(Integer, primary_key=True, autoincrement=True)
    username = Column(String(50), nullable=False, unique=True)  # 用户名
    password = Column(String(255), nullable=False)              # 密码（存储哈希值）
    email = Column(String(100), nullable=False, unique=True)    # 邮箱

    def to_dict(self):
        """
        将用户对象转换为字典，以便 Flask jsonify 调用
        注意：出于安全考虑，永远不要在这里返回 password 字段
        """
        return {
            "id": self.id,
            "username": self.username,
            "email": self.email
        }

    def __repr__(self):
        return f"<User(username='{self.username}', email='{self.email}')>"