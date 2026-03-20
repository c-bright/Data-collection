# app/services/data_service.py
import json
import os
import re
import uuid
import pandas as pd
from typing import List, Dict, Any
from datetime import datetime

from app.models.product_model import Product

from app.utils.database.db_manager import DatabaseManager

# from app.utils.redis_config import RedisClient  # 如需Redis请取消注释
from app.models.product_model import Base

class DataService:
    """
    数据服务类，负责数据清洗、存储等操作
    """

    def __init__(self):
        self.db_manager = DatabaseManager()
        self.db_manager.create_tables(Base)
        # self.redis_client = RedisClient()
        self.target_dir = r"E:\test\smart_data_platform_backend\app\utils"
    # --- 核心入口：供 Pipeline 逐条调用 ---
    def _do_clean_logic(self, item: Dict) -> Dict:
        """
        内部私有方法：统一所有商品数据的字段清洗标准
        """
        return {
            'id': str(uuid.uuid4()),
            'product_id': str(item.get('product_id', '')),
            'name': self.clean_name(item.get('name', '')),
            'price': self.parse_price(item.get('price', 0)),
            'link': item.get('link', ''),
            'image': item.get('image', ''),
            'shop': self.clean_text(item.get('shop', '')),
            'category': self.clean_text(item.get('category', '')),
            'comment_count': self.parse_comment_count(item.get('comment_count', 0))
        }

    # ================= 业务入口 =================
    def process_single_product(self, item: Dict, spider=None) -> bool:
        """
        入口：清洗一条，保存一条。适合 Scrapy 实时处理。
        """
        try:
            cleaned_item = self._do_clean_logic(item)

            return self.save_to_json(cleaned_item)
        except Exception as e:
            if spider:
                spider.logger.error(f"处理数据异常: {str(e)}")
            return False

    # ================= 持久化逻辑 =================
    def save_to_json(self, data: Dict, filename: str = "jd_list.json") -> bool:
        """
        真正的追加模式：每行存一个 JSON 对象
        """
        try:
            # 使用 'a' 模式追加，绝不覆盖
            with open(filename, 'a', encoding='utf-8') as f:
                # 转换为字符串并强制加换行符 \n
                line = json.dumps(data, ensure_ascii=False)
                f.write(line + "\n")
            return True
        except Exception as e:
            print(f"追加写入失败: {e}")
            return False


    def jsonl_to_json_array(self, input_file: str, output_file: str):
        """
        将 JSONL 文件转换为标准的 JSON 数组格式
        """
        data_list = []
        try:
            # 1. 逐行读取 JSONL
            with open(input_file, 'r', encoding='utf-8') as f:
                for line in f:
                    line = line.strip()
                    if line:
                        data_list.append(json.loads(line))

            # 2. 一次性写入标准 JSON 数组
            output_file = os.path.join(self.target_dir, output_file)
            with open(output_file, 'w', encoding='utf-8') as f:
                json.dump(data_list, f, ensure_ascii=False, indent=2)

            if os.path.exists(input_file):
                os.remove(input_file)
                print(f'{input_file}删除成功')
            else:
                print(f'{input_file}删除失败')

            return True

        except Exception as e:
            print(f"转换失败: {e}")
            return False

    def import_products_from_json(self, filename: str = "jd.json") -> bool:
        """
        从标准 JSON 文件读取并批量导入数据库，若 product_id 已存在则忽略
        """
        target_dir = r"E:\test\smart_data_platform_backend\app\utils"
        full_path = os.path.join(target_dir, filename) if not os.path.isabs(filename) else filename

        if not os.path.exists(full_path):
            print(f"错误：找不到文件 {full_path}")
            return False

        session = self.db_manager.get_session()
        try:
            with open(full_path, 'r', encoding='utf-8') as f:
                products_data = json.load(f)

            if not isinstance(products_data, list):
                return False

            # 获取模型所有合法字段名，防止传入多余字段导致 Product(**data) 报错
            valid_columns = {c.name for c in Product.__table__.columns}

            import_count = 0
            skip_count = 0

            for data in products_data:
                # 1. 过滤非法字段
                filtered_data = {k: v for k, v in data.items() if k in valid_columns}
                pid = filtered_data.get('product_id')

                if not pid:
                    continue

                # 2. 【核心逻辑】检查数据库中是否已存在该 product_id
                exists = session.query(Product).filter(Product.product_id == pid).first()

                if exists:
                    # 如果存在，则忽略本次插入
                    skip_count += 1
                    continue

                product_obj = Product(**filtered_data)
                session.add(product_obj)
                import_count += 1

            # 批量提交，提高效率
            session.commit()
            print(f"导入完成：成功插入 {import_count} 条，忽略重复 {skip_count} 条")
            return True

        except Exception as e:
            print(f"批量导入失败: {str(e)}")
            session.rollback()
            return False
        finally:
            self.db_manager.Session.remove()

    def get_formatted_product(self, product_id: str):
        """
        从数据库获取并格式化商品，处理图片链接和价格显示
        """
        # 调用之前修改好的 db_manager 的方法
        p = self.db_manager.get_product_by_id(product_id)

        if not p:
            return None

        return {
            "product_id": p.product_id,
            "name": p.name,
            # 将缩略图 n2 替换为高清图 n0
            "image": p.image.replace('/n2/', '/n0/') if p.image else "",
            "price_display": f"¥{p.price:,.2f}",
            "link": p.link,
            "shop": p.shop,
            "category": p.category,
            "comment_count": f"{p.comment_count / 10000:.1f}万+" if p.comment_count >= 10000 else str(p.comment_count)
        }

    def clean_text(self, text: Any) -> str:
        if not text:
            return ""
        text = str(text).strip()
        text = re.sub(r'[\n\r\t]', ' ', text)
        return text

    def clean_name(self, text: Any) -> str:

        if not text:
            return ""
        text = str(text).strip().replace('\n', '').replace('\r', '').replace('\t', ' ')
        return text

    def parse_price(self, price: Any) -> float:
        if not price:
            return 0.0
        try:
            nums = re.findall(r'\d+\.?\d*', str(price))
            return float(nums[0]) if nums else 0.0
        except:
            return 0.0

    def parse_comment_count(self, count: Any) -> str:
        if not count:
            return "0"

        value_str = str(count)
        try:
            nums = re.findall(r'\d+\.?\d*', value_str)
            if not nums:
                return "0"

            num = float(nums[0])
            # 处理“万”单位
            if '万' in value_str:
                num *= 10000

            return str(int(num))
        except:
            return "0"


class JDReviewProcessor:
    """
    京东评论文件处理类
    功能：
    - 读取 JSON 文件
    - 清洗 tags 和 comments
    - 删除原文件
    - 生成清洗后的 JSON 文件
    """
    def __init__(self, input_file="datil.json", output_file='datil_list.json'):
        self.target_dir = r"E:\test\smart_data_platform_backend\app\utils"
        self.input_file = os.path.join(self.target_dir, input_file)
        self.output_file = os.path.join(self.target_dir, output_file)
        self.data = {}
        self.exclude_tag_keywords = ["全部", "图/视频", "追评", "好评", "中评", "差评"]

    # 读取 JSON 文件
    def read_json(self):
        with open(self.input_file, "r", encoding="utf-8") as f:
            self.data = json.load(f)

    # 清洗 tags
    def clean_tags(self, tags):
        cleaned_tags = []
        for tag in tags:
            name = tag["name"]
            value = tag["value"]
            if any(k in name or k in value for k in self.exclude_tag_keywords):
                continue
            value = value.replace("+", "")
            if "万" in value:
                number = float(value.replace("万", ""))
                value = str(int(number * 10000))
            cleaned_tags.append({"name": name, "value": value})
        return cleaned_tags

    # 清洗单条评论
    def clean_comment(self, comment):
        comment = re.sub(r"[^\u4e00-\u9fffA-Za-z0-9 ]+", "", comment)
        comment = re.sub(r" +", "，", comment)
        return comment

    # 清洗 comments
    def clean_comments(self, comments):
        return [self.clean_comment(c) for c in comments]

    # 执行清洗操作
    def clean_data(self):
        tags = self.data.get("tags", [])
        comments = self.data.get("comments", [])
        cleaned = {
            "tags": self.clean_tags(tags),
            "comments": self.clean_comments(comments)
        }
        return cleaned

    # 删除原文件
    def delete_original(self):
        if os.path.exists(self.input_file):
            os.remove(self.input_file)

    # 保存清洗后的数据
    def save_cleaned(self, cleaned_data):
        with open(self.output_file, "w", encoding="utf-8") as f:
            json.dump(cleaned_data, f, ensure_ascii=False, indent=2)

    # 全流程执行
    def process(self):
        self.read_json()
        cleaned = self.clean_data()
        self.delete_original()
        self.save_cleaned(cleaned)
        print(f"清洗完成，新文件已生成: {self.output_file}")


# # -------------------------------
# # 示例使用
# # -------------------------------
# processor = JDReviewProcessor("jd_bad_comments.json", "jd_bad_comments_cleaned.json")
# processor.process()