
from sqlalchemy import Column, Integer, String, Float, DateTime, Text
from sqlalchemy.ext.declarative import declarative_base
from datetime import datetime

Base = declarative_base()

class Product(Base):
    """
    商品数据模型，用于描述商品基本信息
    """
    __tablename__ = 'products'

    id = Column(Integer, primary_key=True, autoincrement=True)
    product_id = Column(String(100), unique=True, nullable=False)  # 商品ID
    name = Column(String(500), nullable=False)  # 商品名称
    price = Column(Float, nullable=False)  # 商品价格
    link = Column(String(1000))  # 商品链接
    image = Column(String(1000))  # 商品图片
    shop = Column(String(200))  # 店铺名称
    category = Column(String(200))  # 商品分类
    comment_count = Column(Integer)  # 评论数量

    def to_dict(self):
        """
        手动将模型对象转换为字典，解决 jsonify 序列化问题
        """
        return {
            "product_id": self.product_id,
            "name": self.name,
            "price": self.price,
            "link": self.link,
            "image": self.image,
            "shop": self.shop,
            "category": self.category,
            "comment_count": self.comment_count
        }

    def __repr__(self):
        return f"<Product(name='{self.name}', price={self.price})>"