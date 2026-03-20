import scrapy
from ..items import ProductItem
import json
import time
import re
import urllib.parse

from app.crawler.scrapy_spiders.jd_scrapy_demo.jd_scrapy_demo.selenium_spiders.login import JDCrawler
class JdSpider(scrapy.Spider):
    name = "jd"
    allowed_domains = ["jd.com"]

    def __init__(self, keyword="手机", max_page=3, *args, **kwargs):
        super(JdSpider, self).__init__(*args, **kwargs)
        self.keyword = keyword
        self.max_page = int(max_page)

    def start_requests(self):
        kw_quote = urllib.parse.quote(self.keyword)
        self.url = f"https://search.jd.com/Search?keyword={kw_quote}&enc=utf-8&psort=3"
        yield scrapy.Request(
            url=self.url,
            callback=self.parse,
            meta={'use_selenium_list': True, 'page': 1},
            dont_filter=True
        )

    def parse(self, response):
        # 1. 重新定位商品容器（兼容新老版本）
        products = response.xpath('//div[contains(@class, "plugin_goodsCardWrapper")] | //li[contains(@class, "gl-item")]')
        print(len(products))
        for product in products:
            item = ProductItem()

            # 1. SKU (product_id)
            item['product_id'] = product.xpath('./@data-sku').get() or product.xpath('.//@data-sku').get()
            if not item['product_id']:
                continue
            item['name'] = product.xpath('.//*[contains(@class,"_text_")]/@title').get() or \
                           "".join(product.xpath('.//*[contains(@class,"_text_")]//text()').getall()) or ''
            item['price'] = product.xpath('string(.//*[contains(@class,"_price_")])').get() or ''
            item['shop'] = product.xpath('string(.//*[contains(@class,"_name_")])').get() or ''
            item['comment_count'] = product.xpath('string(.//*[contains(@class,"_goods_volume_")])').get() or ''
            img = product.xpath('.//img[contains(@class,"_img_")]/@src').get() or \
                  product.xpath('.//img[contains(@class,"_img_")]/@data-src').get() or ''
            item['image'] = 'https:' + img if img and img.startswith('//') else img or ''
            item['category'] = self.keyword
            item['link'] = f"https://item.jd.com/{item['product_id']}.html" or ''
            yield item

        current_page = response.meta.get('page', 1)
        page_text = response.xpath(
            '//span[contains(@class, "p-skip")]/em/b/text() | //span[@class="fp-text"]/i/text()').get()
        total_pages = int(page_text) if page_text and page_text.isdigit() else self.max_page

        self.logger.info(f"进度: {current_page}/{total_pages}")

        if current_page < total_pages and current_page < self.max_page:
            # 重要：翻页请求依然发往 base_url，中间件会根据 page 自动点下一页
            yield scrapy.Request(
                url=self.url,
                callback=self.parse,
                meta={'use_selenium_list': True, 'page': current_page + 1},
                dont_filter=True
            )