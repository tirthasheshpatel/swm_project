import feedparser
import requests
from bs4 import BeautifulSoup
import time
import matplotlib.pyplot as plt
import numpy as np  # Import numpy for calculating the average
import os  # Import os to check CPU usage
import psutil  # Import psutil to get process CPU usage

def get_rss_feed_data(url):
    # Parse the RSS feed
    feed = feedparser.parse(url)
    
    # Initialize an empty list to store the data
    articles = []
    
    # Initialize a variable to store the number of articles for plotting
    num_articles = 0
    
    # Initialize lists to store parsing times and CPU usages for plotting
    parsing_times = []
    cpu_usages = []  # List to store CPU usages
    
    # Get the current process id and process object for CPU usage measurement
    pid = os.getpid()
    p = psutil.Process(pid)
    
    # Loop through each entry in the RSS feed
    for entry in feed.entries:
        # Extract the required information
        title = entry.title
        author = entry.get("author", "No author")
        article_url = entry.link
        published_date = entry.published
        
        # Start measuring time and CPU usage
        start_time = time.time()
        start_cpu_usage = p.cpu_percent(interval=None)  # Get the current process CPU usage
        
        # Fetch the article content and extract the first 100 characters
        response = requests.get(article_url)
        soup = BeautifulSoup(response.content, 'html.parser')
        text = soup.get_text(strip=True)[:100]  # Get the first 100 characters of the text
        
        # Calculate parsing time and append it to the list
        parsing_time = time.time() - start_time
        parsing_times.append(parsing_time)
        
        # Calculate CPU usage and append it to the list
        end_cpu_usage = p.cpu_percent(interval=None)  # Get the process CPU usage after parsing
        cpu_usage = round(end_cpu_usage - start_cpu_usage, 5)  # Calculate CPU usage accurate to 5 decimal places
        cpu_usages.append(cpu_usage)
        
        # Increment the number of articles
        num_articles += 1
        
        # Append the information as a dictionary to the articles list
        articles.append({
            "Title": title,
            "Author": author,
            "URL": article_url,
            "Published Date": published_date,
            "Text": text,
            "Parsing Time": parsing_time,
            "CPU Usage": cpu_usage  # Add CPU usage to the dictionary
        })
    
    return articles, num_articles, parsing_times, cpu_usages  # Return CPU usages as well

# RSS feed URLs
rss_feed_urls = [
    "https://rss.nytimes.com/services/xml/rss/nyt/US.xml",
    "https://feeds.a.dj.com/rss/RSSOpinion.xml",
    "https://feeds.a.dj.com/rss/RSSWorldNews.xml",
    "https://feeds.a.dj.com/rss/WSJcomUSBusiness.xml",
    "https://feeds.a.dj.com/rss/RSSMarketsMain.xml",
    "https://feeds.a.dj.com/rss/RSSWSJD.xml",
    "https://feeds.a.dj.com/rss/RSSLifestyle.xml"
]

# Get the data from the RSS feeds and plot
plt.figure(figsize=(15, 10))
cpu_info = psutil.cpu_percent(interval=None)  # Get CPU info to display on the graph
for index, rss_feed_url in enumerate(rss_feed_urls):
    data, num_articles, parsing_times, cpu_usages = get_rss_feed_data(rss_feed_url)  # Include CPU usages in the returned values
    average_parsing_time = np.mean(parsing_times)
    average_cpu_usage = np.mean(cpu_usages)  # Calculate the average CPU usage
    
    # Create subplot for each RSS feed
    plt.subplot(len(rss_feed_urls), 1, index + 1)
    plt.barh(f'Website {index + 1} ({num_articles} articles)', parsing_times, color=np.random.rand(3,))
    plt.xlabel('Parsing Time (s) and Average CPU Usage')
    plt.ylabel('Website')
    plt.title(f'Parsing Time for {rss_feed_url} (Average: {average_parsing_time:.2f} seconds, CPU Usage: {average_cpu_usage:.5f})')  # Display CPU usage accurate to 5 decimal places in the title

# Mention the CPU configuration in the upper left corner of the graph
cpu_model = psutil.cpu_freq().current  # Get the current CPU frequency for configuration
plt.figtext(0.01, 0.99, f'CPU Configuration: {cpu_model} MHz', ha="left", va="top", fontsize=10, bbox={"facecolor":"orange", "alpha":0.5, "pad":5})

plt.tight_layout()
plt.show()


