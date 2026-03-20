import json
import os
from typing import Dict, Any

from app.analysis.product_stats_analyzer import ProductStatsAnalyzer
from app.analysis.comment_analyzer import CommentAnalyzer
from app.analysis.TagAnalyzer import TagAnalyzer


class FrontendDataService:
    def __init__(self, json_file="jd_scatter_comment.json"):
        self.target_dir = r"E:\test\smart_data_platform_backend\app\utils"
        self.json_file = os.path.join(self.target_dir, json_file)
        self.output_file = os.path.join(self.target_dir, "da.json")
        self.data = self.load_json()

    def load_json(self) -> Dict[str,Any]:
        with open(self.json_file, "r", encoding="utf-8") as f:
            return json.load(f)

    def generate_frontend_data(self) -> Dict[str,Any]:
        #  商品数据
        product_analyzer = ProductStatsAnalyzer(self.data.get("scatter_data", []))
        product_stats = {
            "scatter_points": product_analyzer.scatter_points(),
            "price_distribution": product_analyzer.price_distribution(),
            "shop_distribution": product_analyzer.shop_distribution()
        }

        # ️ 差评数据
        comment_analyzer = CommentAnalyzer(self.data.get("comments", []))
        comments_stats = {
            "negative_wordcloud": comment_analyzer.negative_wordcloud()
        }

        # 3 标签数据（优点）
        tag_analyzer = TagAnalyzer(self.data.get("tags",[]))
        tag_stats = tag_analyzer.tag_stats()

        # 汇总
        frontend_data = {
            "product": product_stats,
            "comments": comments_stats,
            "tags": tag_stats
        }

        return frontend_data
    def save_frontend_json(self):
        data = self.generate_frontend_data()
        os.makedirs(os.path.dirname(self.output_file), exist_ok=True)
        with open(self.output_file, "w", encoding="utf-8") as f:
            json.dump(data, f, ensure_ascii=False, indent=2)
        print(f"前端可视化数据已生成：{self.output_file}")
        return data