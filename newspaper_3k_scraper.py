from newspaper import Article

article_url = 'https://www.cnn.com/2024/03/31/politics/mike-johnson-motion-to-vacate-ukraine-funding/index.html'

article = Article(article_url)
article.download()

print(f"Title: {article.title}")
print(f"Content: {article.text[:100]}...")
print(f"Authors: {', '.join(article.authors)}")
print(f"Publish Date: {article.publish_date.strftime('%Y-%m-%d')}")
print(f"URL: {article.url}")
