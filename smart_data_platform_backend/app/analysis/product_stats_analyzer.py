from typing import List, Dict, Any

class ProductStatsAnalyzer:
    """
    商品统计分析类
    用于分析价格区间、店铺分布、散点图数据
    """

    def __init__(self, scatter_data: List[Dict[str, Any]]):
        self.scatter_data = scatter_data

    def price_distribution(self) -> Dict[str, int]:
        """
        统计商品价格区间
        """
        ranges = {
            "0-500元": 0,
            "500-1000元": 0,
            "1000-3000元": 0,
            "3000元以上": 0
        }

        for item in self.scatter_data:
            price = float(item["price"])

            if price <= 500:
                ranges["0-500元"] += 1
            elif price <= 1000:
                ranges["500-1000元"] += 1
            elif price <= 3000:
                ranges["1000-3000元"] += 1
            else:
                ranges["3000元以上"] += 1

        return ranges

    def shop_distribution(self) -> Dict[str, int]:
        """
        统计不同店铺商品数量
        """
        shop_count = {}

        for item in self.scatter_data:
            shop = item["shop"]
            shop_count[shop] = shop_count.get(shop, 0) + 1

        return shop_count

    def scatter_points(self) -> List[Dict[str, Any]]:
        """
        返回散点图数据（价格 vs 评论数）
        """
        return [
            {
                "price": float(i["price"]),
                "comment": int(i["comment"]),
                "shop": i["shop"]
            }
            for i in self.scatter_data
        ]
