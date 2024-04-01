import scrapy
from datetime import datetime
from cnn_scraper_demo.items import CnnScraperDemoItem


class CnnArticleSpider(scrapy.Spider):
    name = 'cnn_article'
    allowed_domains = ['cnn.com']
    start_urls = ['https://www.cnn.com/2024/03/31/politics/mike-johnson-motion-to-vacate-ukraine-funding/index.html']

    def parse(self, response):
        item = CnnScraperDemoItem()

        # Extract article title
        title = response.css('h1.headline__text::text').get().strip()
        item['title'] = title

        # Extract article content
        content_paragraphs = response.css('div.article__content p::text').getall()
        content = ' '.join(content_paragraphs).strip()
        item['content'] = content

        # Extract authors
        authors = response.css('span.byline__name::text').getall()
        item['authors'] = authors

        # Extract publish date
        publish_date_str = response.css('div.timestamp::text').get().strip().split()[-7:]
        publish_date_str.pop(2)  # remove timezone information since datetime can't parse it
        item['publish_date'] = datetime.strptime(" ".join(publish_date_str), "%I:%M %p %a %B %d, %Y")

        # Extract article URL
        url = response.url
        item['url'] = url

        yield item
