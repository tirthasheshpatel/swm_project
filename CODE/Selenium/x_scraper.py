
import time
from bs4 import BeautifulSoup
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
import pandas as pd
import re

# Initiate chrome webdriver
driver = webdriver.Chrome()
driver.maximize_window()

# Enter twitter URL
url = 'https://twitter.com/login'
driver.get(url)
time.sleep(4)

## Create a text file 'credentials.txt' and add twitter username in the first row and password in the second row
# Load username from the first row of credentials.txt
username = driver.find_element(By.XPATH, '//*[@id="layers"]/div/div/div/div/div/div/div[2]/div[2]/div/div/div[2]/div[2]/div/div/div/div[5]/label/div/div[2]/div/input')
username.send_keys([line.rstrip('\n') for line in open('credentials.txt')][0])

next_button = driver.find_element(By.XPATH, '//*[@id="layers"]/div/div/div/div/div/div/div[2]/div[2]/div/div/div[2]/div[2]/div/div/div/div[6]')
next_button.click()
time.sleep(4)

# Load password from the second row of credentials.txt
password = driver.find_element(By.XPATH, '//*[@id="layers"]/div/div/div/div/div/div/div[2]/div[2]/div/div/div[2]/div[2]/div[1]/div/div/div[3]/div/label/div/div[2]/div[1]/input')
password.send_keys([line.rstrip('\n') for line in open('credentials.txt')][1])

# Locate the login button and sign in to twitter
login = driver.find_element(By.XPATH, '//*[@id="layers"]/div/div/div/div/div/div/div[2]/div[2]/div/div/div[2]/div[2]/div[2]/div/div[1]/div/div/div')
login.click()
time.sleep(3)

# Locate the search box on the home page and prepare for keyword search queries input
first_search = driver.find_element(By.XPATH, '//*[@id="react-root"]/div/div/div[2]/main/div/div/div/div[2]/div/div[2]/div/div/div/div[1]/div/div/div/form/div[1]/div/div/div/label/div[2]/div/input')
first_search.send_keys('CNN Breaking News since:2019-10-03 until:2019-10-10')
first_search.send_keys(Keys.ENTER)
time.sleep(2)

# SECTION B - TWEET LOADING AND SCRAPING

# Use regex to extract tweet features including username, userhandle, post date and tweet text
user_name = re.compile(r'.+?@')
user_handle = re.compile(r'@.+?·')
post_date = re.compile(r'·[A-z][a-z][a-z].+?, [0-9][0-9][0-9][0-9]')
tweet_text = re.compile(r', [0-9][0-9][0-9][0-9].+')

# Empty dictionary to store tweet features
twitter_data = {}
tweet_count = 0

# Iterating over the list of queries generated from Twitter_Query_Generator.py
while tweet_count < 100:
    start_scrape_time = time.monotonic()
    source = driver.page_source
    soup = BeautifulSoup(source, 'html.parser')
    tweet_data = soup.find_all('article', {'aria-haspopup': 'false'})
    tweet_data = soup.find_all('article', {'role': 'article'})

    tweet_dup = []

    for tweet_du in tweet_data:
        tweet_dup.append(tweet_du)

    for new_article in tweet_data:
        all_text = new_article.text
        try:
            user = re.findall(user_name, all_text)[0]
            user = user[:-1]
        except:
            user = 'N/A'
        try:
            handle = re.findall(user_handle, all_text)[0]
            handle = handle[:-1]
            replace = re.sub("@", "/", handle)
            true_handle = 'https://twitter.com' + replace
        except:
            true_handle = 'N/A'
        try:
            date = re.findall(post_date, all_text)[0]
        except:
            date = 'N/A'

        try:
            tweet_find = re.findall(tweet_text, all_text)[0]
            tweet_http = re.sub(', [0-9][0-9][0-9][0-9]', '', tweet_find)
            tweet = re.sub(
                'https?:\/\/(?:www\.|(?!www))[a-zA-Z0-9][a-zA-Z0-9-]+[a-zA-Z0-9]\.[^\s]{2,}|www\.[a-zA-Z0-9][a-zA-Z0-9-]+[a-zA-Z0-9]\.[^\s]{2,}|https?:\/\/(?:www\.|(?!www))[a-zA-Z0-9]+\.[^\s]{2,}|www\.[a-zA-Z0-9]+\.[^\s]{2,}',
                '', tweet_http)
        except:
            tweet = 'N/A'

        tweet_count += 1
        end_scrape_time = time.monotonic()
        duration = end_scrape_time - start_scrape_time
        twitter_data[tweet_count] = [user, true_handle, date, tweet, duration]

    # Tweets do not load unless page is scrolled down. To counter this issue 'JavaScript injection' was used
    driver.execute_script("window.scrollTo(0, document.body.scrollHeight);")
    time.sleep(2)
    driver.execute_script("window.scrollBy(0, -2)")
    driver.execute_script("window.scrollBy(0, 3)")
    driver.execute_script("window.scrollBy(0, -2)")
    time.sleep(2)
    driver.execute_script("window.scrollTo(0, document.body.scrollHeight);")

# Save scraped data to a csv file
try:
    twitter_df = pd.DataFrame.from_dict(twitter_data, orient='index',
                                        columns=['Username', 'Handle', 'Published', 'Tweet', 'Duration'])
    twitter_df['Username'] = twitter_df['Username'].map(
        lambda x: x.encode('unicode-escape').decode('utf-8'))
    twitter_df['Handle'] = twitter_df['Handle'].map(
        lambda x: x.encode('unicode-escape').decode('utf-8'))
    twitter_df['Published'] = twitter_df['Published'].map(
        lambda x: x.encode('unicode-escape').decode('utf-8'))
    twitter_df['Tweet'] = twitter_df['Tweet'].map(
        lambda x: x.encode('unicode-escape').decode('utf-8'))
    twitter_df.to_csv('SeleniumXResults.csv', index=False)  # Rename the file here
except Exception as e:
    print(e)
