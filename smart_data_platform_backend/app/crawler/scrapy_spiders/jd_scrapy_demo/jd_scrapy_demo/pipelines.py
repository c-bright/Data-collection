# Define your item pipelines here
#
# Don't forget to add your pipeline to the ITEM_PIPELINES setting
# See: https://docs.scrapy.org/en/latest/topics/item-pipeline.html


# useful for handling different item types with a single interface

from itemadapter import ItemAdapter

import sys
import os
import uuid
import time
from datetime import datetime
import json

# --- 核心路径修复 ---
current_path = os.path.abspath(__file__)
# 向上推 5 级到达根目录 smart_data_platform_backend
root_path = os.path.dirname(os.path.dirname(os.path.dirname(os.path.dirname(os.path.dirname(os.path.dirname(current_path))))))

if root_path not in sys.path:
    sys.path.insert(0, root_path)

from itemadapter import ItemAdapter
from app.services.data_service import DataService
from app.models.product_model import Product



class DatabasePipeline:
    def __init__(self):
        # 实例化 DataService，它包含了数据库管理器
        self.data_service = DataService()

    def process_item(self, item, spider):
        item_dict = ItemAdapter(item).asdict()

        # 2. 交给 service 执行 [清洗 -> 转换 -> 保存]
        success = self.data_service.process_single_product(item_dict, spider)

        if success:
            spider.logger.debug(f"SKU {item_dict.get('product_id')} 处理成功")

        return item
    def close_spider(self, spider):
        self.data_service.jsonl_to_json_array(input_file='jd_list.json', output_file='jd.json')
        self.data_service.import_products_from_json()

class JsonPipeline:
    def open_spider(self, spider):
        self.file = open('jd_data.json', 'w', encoding='utf-8')
        self.file.write('[\n')
        self.first_item = True

    def close_spider(self, spider):
        self.file.write('\n]')
        self.file.close()

    def process_item(self, item, spider):
        line = json.dumps(ItemAdapter(item).asdict(), ensure_ascii=False, indent=2)

        if not self.first_item:
            self.file.write(',\n')
        else:
            self.first_item = False

        self.file.write(line)
        return item