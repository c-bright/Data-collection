import os
import sys
from pathlib import Path

from scrapy.crawler import CrawlerProcess
from scrapy.utils.project import get_project_settings

from app.crawler.scrapy_spiders.jd_scrapy_demo.jd_scrapy_demo.spiders.jd import JdSpider

CURRENT_DIR = Path(__file__).resolve().parent
PROJECT_ROOT = CURRENT_DIR.parent.parent.parent.parent.parent

if str(PROJECT_ROOT) not in sys.path:
    sys.path.insert(0, str(PROJECT_ROOT))

os.environ.setdefault(
    "SCRAPY_SETTINGS_MODULE",
    "app.crawler.scrapy_spiders.jd_scrapy_demo.jd_scrapy_demo.settings"
)

class JdCrawler:
    def __init__(self, keyword, max_page):

        self.keyword = keyword
        self.max_page = max_page
        self.process = CrawlerProcess(get_project_settings())

    def run(self):

        self.process.crawl(JdSpider, keyword=self.keyword, max_page=self.max_page)
        self.process.start()

# 使用示例
if __name__ == "__main__":
    crawler = JdCrawler(keyword="电脑", max_page=3)
    crawler.run()
