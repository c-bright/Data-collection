

import os
import configparser
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker, scoped_session
from sqlalchemy.exc import SQLAlchemyError
from app.models.product_model import Product

class DatabaseManager:
    def __init__(self, config_file: str = None):
        self.base_dir = os.path.dirname(os.path.abspath(__file__))

        if config_file is None:
            config_file = os.path.join(self.base_dir, "config.ini")

        config = configparser.ConfigParser()
        config.read(config_file, encoding="utf-8")
        db = config["mysql"]

        db_url = f"mysql+pymysql://{db.get('user')}:{db.get('password')}@{db.get('host')}:{db.get('port')}/{db.get('database')}?charset={db.get('charset', 'utf8mb4')}"

        # 3. 创建引擎与 Session
        self.engine = create_engine(db_url, pool_size=10, max_overflow=20, pool_pre_ping=True)
        self.session_factory = sessionmaker(bind=self.engine)
        self.Session = scoped_session(self.session_factory)  # 线程安全

        print("SQLAlchemy 数据库连接成功")

    def get_session(self):
        return self.Session()

    # --- 核心业务方法 ---

    def create_tables(self, Base):
        """根据模型创建所有缺失的表"""
        try:
            Base.metadata.create_all(self.engine)
            print("数据表检查/创建完成")
        except Exception as e:
            print(f"创建表失败: {e}")

    def insert_product(self, product_data: dict):
        """插入单条商品数据"""
        session = self.get_session()
        try:
            # 这种写法会自动处理字段映射，非常安全
            new_product = Product(**product_data)
            session.merge(new_product)  # 使用 merge 如果主键/唯一键冲突则更新，不冲突则插入
            session.commit()
        except SQLAlchemyError as e:
            session.rollback()
            print(f"数据插入失败: {e}")
        finally:
            self.Session.remove()

    def get_product_by_id(self, product_id: str):
        """根据 product_id 查询商品"""
        session = self.get_session()
        try:
            # 使用 filter 配合 .first() 查询
            return session.query(Product).filter(Product.product_id == product_id).first()
        finally:
            self.Session.remove()

    def select_all_products(self, limit=50):
        """获取商品列表供前端展示"""
        session = self.get_session()
        try:

            return session.query(Product).order_by(Product.id.desc()).limit(limit).all()
        finally:
            self.Session.remove()

    def get_formatted_product(self, product_id: str):
        """
        查询并直接返回字典格式，方便 API 调用
        """
        session = self.get_session()
        try:
            product = session.query(Product).filter(Product.product_id == str(product_id)).first()
            return product.to_dict() if product else None
        except Exception as e:
            print(f"查询失败: {e}")
            return None
        finally:
            self.Session.remove()

    def update_product_attributes(self, product_id: str, attributes: dict):
        """
        专门用于更新爬虫抓取到的详细规格参数 (JSON 字段)
        """
        session = self.get_session()
        try:
            product = session.query(Product).filter(Product.product_id == str(product_id)).first()
            if product:
                product.attributes = attributes  # 修改对象属性
                session.commit()
                print(f"商品 {product_id} 属性更新成功")
                return True
            return False
        except SQLAlchemyError as e:
            session.rollback()
            print(f"属性更新失败: {e}")
            return False
        finally:
            self.Session.remove()

    def close(self):
        """释放连接池"""
        self.engine.dispose()
        print("数据库连接池已关闭")