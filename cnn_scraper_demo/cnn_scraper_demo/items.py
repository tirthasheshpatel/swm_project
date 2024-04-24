# Define here the models for your scraped items
#
# See documentation in:
# https://docs.scrapy.org/en/latest/topics/items.html

import scrapy


class CnnScraperDemoItem(scrapy.Item):
    title = scrapy.Field()
    content = scrapy.Field()
    authors = scrapy.Field()
    publish_date = scrapy.Field()
    url = scrapy.Field()

class NytArticleItem(scrapy.Item):
    title = scrapy.Field()
    link = scrapy.Field()
    description = scrapy.Field()
    pub_date = scrapy.Field()
    parse_time = scrapy.Field()