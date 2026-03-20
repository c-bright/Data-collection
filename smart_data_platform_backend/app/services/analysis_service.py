import json
from typing import List, Dict, Any
import os
import re

class ScatterCommentService:
    """
    生成商品散点数据与评论结合的 JSON，并保留标签
    """

    def __init__(self, product_file="jd.json", review_file='datil_list.json'):
        self.target_dir = r"E:\test\smart_data_platform_backend\app\utils"
        self.product_file = os.path.join(self.target_dir, product_file)
        self.review_file = os.path.join(self.target_dir, review_file)
        self.product_data: List[Dict[str, Any]] = []
        self.review_data: Dict[str, Any] = {}
        self.load_data()
        self.output_file = os.path.join(self.target_dir, "jd_scatter_comment.json")

    def load_data(self):
        """加载商品和评论 JSON"""
        with open(self.product_file, "r", encoding="utf-8") as f:
            self.product_data = json.load(f)
        with open(self.review_file, "r", encoding="utf-8") as f:
            self.review_data = json.load(f)

    def _clean_text(self, text: str) -> str:
        """清洗评论文本，只保留汉字、字母、数字"""
        text = re.sub(r"[^\u4e00-\u9fffA-Za-z0-9 ]+", "", text)
        text = re.sub(r" +", " ", text)
        return text

    def generate_scatter_comment_json(self) -> Dict[str, Any]:
        # 生成散点数据
        scatter_data = []
        for p in self.product_data:
            try:
                scatter_data.append({
                    "price": float(p.get("price", 0)),
                    "comment": int(p.get("comment_count", 0)),
                    "shop": p.get("shop", "")
                })
            except:
                continue

        # 清洗评论
        comments = self.review_data.get("comments", [])
        cleaned_comments = [self._clean_text(c) for c in comments if c.strip()]

        # 保留 tags
        tags = self.review_data.get("tags", [])

        # 合并成一个字典
        result = {
            "scatter_data": scatter_data,
            "comments": cleaned_comments,
            "tags": tags
        }
        return result

    def save_json(self):
        result = self.generate_scatter_comment_json()
        os.makedirs(os.path.dirname(self.output_file), exist_ok=True)
        with open(self.output_file, "w", encoding="utf-8") as f:
            json.dump(result, f, ensure_ascii=False, indent=2)
        print(f"JSON 已生成并保存：{self.output_file}")

        if os.path.exists(self.review_file) and os.path.exists(self.output_file):
            os.remove(self.review_file)
            print(f"原评论文件已删除：{self.review_file}, {self.review_file}")



if __name__ == "__main__":
    service = ScatterCommentService()
    service.save_json()