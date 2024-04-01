import requests
from bs4 import BeautifulSoup
from datetime import datetime


class Article:
    def __init__(self, title, content, authors, publish_date, url):
        self.title = title
        self.content = content
        self.authors = authors
        self.publish_date = publish_date
        self.url = url


def scrape_article(url):
    response = requests.get(url)
    response.raise_for_status()
    soup = BeautifulSoup(response.content, "html.parser")

    # Extract article title
    title = soup.find("h1", {"class": "headline__text"}).text.strip()

    # Extract article content
    content_div = soup.find("div", {"class": "article__content"})
    content = " ".join([p.text.strip() for p in content_div.find_all("p")])

    # Extract authors
    authors = [author.text.strip() for author in soup.find_all("span", {"class": "byline__name"})]

    # Extract publish date
    publish_date_str = soup.find("div", {"class": "timestamp"}).text.strip().split()[-7:]
    publish_date_str.pop(2)  # remove timezone information since datetime can't parse it
    publish_date = datetime.strptime(" ".join(publish_date_str), "%I:%M %p %a %B %d, %Y")

    return Article(title, content, authors, publish_date, url)


# Example usage
article_url = "https://www.cnn.com/2024/03/31/politics/mike-johnson-motion-to-vacate-ukraine-funding/index.html"
article = scrape_article(article_url)

if article:
    print(f"Title: {article.title}")
    print(f"Content: {article.content[:100]}...")
    print(f"Authors: {', '.join(article.authors)}")
    print(f"Publish Date: {article.publish_date.strftime('%Y-%m-%d')}")
    print(f"URL: {article.url}")
