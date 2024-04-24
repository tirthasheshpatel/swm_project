import logging
import scrapy
from datetime import datetime
import time
from cnn_scraper_demo.items import NytArticleItem


class NytSpider(scrapy.Spider):
    name = 'nyt_rss_feed'
    allowed_domains = ['nytimes.com']
    start_urls = ['https://rss.nytimes.com/services/xml/rss/nyt/US.xml']
    articles_scraped = 0
    MAX_ARTICLES = 100


    def parse(self, response):
        logging.info('Parsing started...')

        items = []

        # Extracting data from RSS feed items
        for item in response.xpath('//item'):
            start_time = time.time()
            nyt_rss_item = NytArticleItem()
            nyt_rss_item['title'] = item.xpath('title/text()').extract_first()
            nyt_rss_item['link'] = item.xpath('link/text()').extract_first()
            nyt_rss_item['description'] = item.xpath('description/text()').extract_first()
            nyt_rss_item['pub_date'] = item.xpath('pubDate/text()').extract_first()
            end_time = time.time()  # End time for parsing the current entry
            parse_time = end_time - start_time  # Calculate the time taken to parse the current entry
            nyt_rss_item['parse_time'] = parse_time  # Add parse time to the item
            items.append(nyt_rss_item)
            self.articles_scraped += 1
            if self.articles_scraped >= self.MAX_ARTICLES:
                break

        return items
