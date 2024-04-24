import scrapy
from cnn_scraper_demo.items import CnnRssArticleItem
import time

class CNNSpider(scrapy.Spider):
    name = 'css_rss_spider'
    start_urls = ['http://rss.cnn.com/rss/cnn_topstories.rss']
    articles_scraped = 0
    MAX_ARTICLES = 100

    def parse(self, response):
        items = []

        # Extracting data from RSS feed items
        for item in response.xpath('//item'):
            start_time = time.time()
            cnn_rss_item = CnnRssArticleItem()
            cnn_rss_item['title'] = item.xpath('title/text()').extract_first()
            cnn_rss_item['link'] = item.xpath('link/text()').extract_first()
            cnn_rss_item['description'] = item.xpath('description/text()').extract_first()
            cnn_rss_item['pub_date'] = item.xpath('pubDate/text()').extract_first()
            end_time = time.time()  # End time for parsing the current entry
            parse_time = end_time - start_time  # Calculate the time taken to parse the current entry
            cnn_rss_item['parse_time'] = parse_time  # Add parse time to the item
            items.append(cnn_rss_item)
            self.articles_scraped += 1
            if self.articles_scraped >= self.MAX_ARTICLES:
                break

        return items
