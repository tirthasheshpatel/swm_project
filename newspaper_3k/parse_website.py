import newspaper 
import time
import pandas as pd
from tqdm import tqdm
import feedparser 

def time_it(func):
    """Decorator to measure the execution time of a function."""
    def wrapper(*args, **kwargs):
        start_time = time.time() 
        result = func(*args, **kwargs) 
        end_time = time.time()
        duration = end_time - start_time
        print(f"Executing {func.__name__}: {duration:.4f} seconds")
        return result
    return wrapper

class NewsParser:

    def __init__(self) -> None:
        self.article_list = []
        self.result_df = pd.DataFrame(columns=['title', 'authors', 'publish_date', 'text', 'url', 'duration'])
        

    def parse_article(self, article_url):
        start_time = time.time()
        article = newspaper.Article(url=article_url)
        article.download()
        article.parse()
        time_taken = time.time() - start_time

        return {
            'title' : article.title,
            'authors' : article.authors,
            'publish_date' : article.publish_date,
            'text' : article.text[:100],
            'url' : article.url, 
            'duration' : time_taken
        }
    
    def parse_all_articles(self):
        self.init_article_list()
        print(f"Parsing newspaper of size: {len(self.article_list)}")
        for article_url in tqdm(self.article_list):
            try:
                res = self.parse_article(article_url=article_url)
                self.result_df = pd.concat([self.result_df, pd.DataFrame(res)])

            except Exception as e:
                print(e)
                print(f"Unable to download {article_url}")

    def init_article_list(self):
        pass

class ParseWebsite(NewsParser):
    def __init__(self, url, num_articles=None) -> None:
        self.url = url
        self.build_newspaper()
        self.num_articles = num_articles
        self.result_df = pd.DataFrame(columns=['title', 'authors', 'publish_date', 'text', 'url', 'duration'])
        self.article_list = []

    @time_it
    def build_newspaper(self):
        self.parser = newspaper.build(self.url, memoize_articles=False)

    def init_article_list(self):
        articles_to_parse = self.parser.articles[:self.num_articles] if self.num_articles else self.parser.articles[:10]
        for article in  articles_to_parse:
            self.article_list.append(article.url)
        print(self.article_list)



class ParseRSS(NewsParser):
    def __init__(self, url, num_articles) -> None:
        super().__init__()
        self.url = url
        self.num_articles = num_articles
        self.article_list = []
    
    def init_article_list(self):
        for url in self.url:
            feed = feedparser.parse(url)
            for entry in feed.entries:
                self.article_list.append(entry.link)
        self.article_list = self.article_list[:self.num_articles] if self.num_articles else self.article_list[:10]








if __name__ == "__main__":
    web_parser = ParseRSS(
        url=[
                "https://news.google.com/rss?hl=en-US&gl=US&ceid=US:en"
            ], num_articles=100)
    web_parser.parse_all_articles()
    web_parser.result_df.to_csv("google_result.csv")



            
