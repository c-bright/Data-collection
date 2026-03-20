import scrapy
from scrapy.crawler import CrawlerProcess
import csv
import os
import random
import time

# 数据保存路径
DATA_FILE = os.path.join(os.path.dirname(__file__), "../../data/jd_products.csv")

class JDSpider(scrapy.Spider):
    name = "jd_spider"
    # 搜索关键字“手机”为例
    start_urls = ["https://search.jd.com/Search?keyword=手机&enc=utf-8"]
    max_products = 300  # 控制抓取量

    products = []

    def parse(self, response):
        # 京东商品列表 li.gl-item
        for product in response.css("li.gl-item"):
            title_parts = product.css("div.p-name a em::text").getall()
            title = "".join(title_parts).strip()
            link = product.css("div.p-name a::attr(href)").get()
            link = response.urljoin(link)
            shop = product.css("div.p-shop a::attr(title)").get()
            # 简单处理分类（可选）
            category = response.css("div#J_selector a::text").getall()
            category = " > ".join([c.strip() for c in category if c.strip()])

            self.products.append({
                "title": title,
                "link": link,
                "shop": shop,
                "category": category
            })

            # 控制总数
            if len(self.products) >= self.max_products:
                break

        # 翻页
        if len(self.products) < self.max_products:
            next_page = response.css("a.pn-next::attr(href)").get()
            if next_page:
                time.sleep(random.uniform(1, 2))  # 避免被封
                yield response.follow(next_page, self.parse)

    @classmethod
    def run(cls):
        process = CrawlerProcess()
        process.crawl(cls)
        process.start()

        # 保存 CSV
        os.makedirs(os.path.dirname(DATA_FILE), exist_ok=True)
        with open(DATA_FILE, "w", newline="", encoding="utf-8") as f:
            writer = csv.DictWriter(f, fieldnames=["title", "link", "shop", "category"])
            writer.writeheader()
            for p in cls.products:
                writer.writerow(p)
        print(f"爬取完成，共 {len(cls.products)} 条商品，保存在 {DATA_FILE}")
if __name__ == "__main__":
    JDSpider.run()