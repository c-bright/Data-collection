from typing import List, Dict, Any


class TagAnalyzer:
    """
    商品标签分析类
    用于统计商品优点标签
    """

    def __init__(self, tags: List[Dict[str, Any]]):
        self.tags = tags

    def tag_stats(self) -> List[Dict]:
        """
        统计标签并按数量排序
        """
        result = []

        for tag in self.tags:
            result.append({
                "name": tag["name"],
                "value": int(tag["value"])   # 直接转整数
            })

        # 按 value 从大到小排序
        return sorted(result, key=lambda x: x["value"], reverse=True)