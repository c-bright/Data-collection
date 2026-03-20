# Define here the models for your scraped items
#
# See documentation in:
# https://docs.scrapy.org/en/latest/topics/items.html

import scrapy


class ProductItem(scrapy.Item):
    # 商品ID
    product_id = scrapy.Field()
    # 名称
    name = scrapy.Field()
    # 店铺
    shop = scrapy.Field()
    # 价格
    price = scrapy.Field()
    # 类别
    category = scrapy.Field()
    # 评论总数
    comment_count = scrapy.Field()
    # 商品链接
    link = scrapy.Field()
    # 商品图片
    image = scrapy.Field()


