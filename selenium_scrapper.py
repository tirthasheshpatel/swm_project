from selenium import webdriver
from selenium.webdriver.common.by import By
from datetime import datetime

class Article:
    def __init__(self, title, content, authors, publish_date, url):
        self.title = title
        self.content = content
        self.authors = authors
        self.publish_date = publish_date
        self.url = url


def scrape_article(url):
    try:
        # Initialize the webdriver (e.g., Chrome or Firefox)
        driver = webdriver.Chrome()  # or webdriver.Firefox()

        # Navigate to the article URL
        driver.get(url)

        # Extract article title
        title_element = driver.find_element(By.CSS_SELECTOR, "h1.headline__text")
        title = title_element.text.strip()

        # Extract article content
        content_element = driver.find_element(By.CSS_SELECTOR, "div.article__content")
        content = " ".join([p.text.strip() for p in content_element.find_elements(By.TAG_NAME, "p")])

        # Extract authors
        author_elements = driver.find_elements(By.CSS_SELECTOR, "span.byline__name")
        authors = [author.text.strip() for author in author_elements]

        # Extract publish date
        publish_date_str = driver.find_element(By.CSS_SELECTOR, "div.timestamp").text.strip().split()[-7:]
        publish_date_str.pop(2)  # remove timezone information since datetime can't parse it
        publish_date = datetime.strptime(" ".join(publish_date_str), "%I:%M %p %a %B %d, %Y")

        return Article(title, content, authors, publish_date, url)
    finally:
        if driver:
            driver.quit()

# Example usage
article_url = "https://www.cnn.com/2024/03/31/politics/mike-johnson-motion-to-vacate-ukraine-funding/index.html"
article = scrape_article(article_url)

if article:
    print(f"Title: {article.title}")
    print(f"Content: {article.content[:100]}...")
    print(f"Authors: {', '.join(article.authors)}")
    print(f"Publish Date: {article.publish_date.strftime('%Y-%m-%d')}")
    print(f"URL: {article.url}")
