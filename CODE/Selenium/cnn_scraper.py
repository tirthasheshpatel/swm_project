from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from bs4 import BeautifulSoup
import csv
import time

# Function to initialize Selenium webdriver
def init_driver():
    driver = webdriver.Chrome()  # Assuming Chrome is installed, you may need to change this based on your browser
    return driver

# Function to extract news using Selenium
def extract_news(driver, query):
    driver.get("https://www.cnn.com/search?q=" + query)
    time.sleep(2)  # Wait for page to load

    # Get page source
    page_source = driver.page_source
    return page_source

# Function to parse page source using Beautiful Soup
def parse_page_source(page_source):
    soup = BeautifulSoup(page_source, 'html.parser')
    articles = soup.find_all('div', class_='card container__item')

    data = []
    for article in articles:
        link = article.find('a', class_='container__link')['href']
        title = article.find('span', class_='container__headline-text').text.strip()
        time_ago = article.find('div', class_='container__date').text.strip()
        description = article.find('div', class_='container__description').text.strip()
        data.append([title, link, time_ago, description])

    return data

# Function to save data to CSV
def save_to_csv(data, filename):
    with open(filename, 'w', newline='', encoding='utf-8') as csvfile:
        writer = csv.writer(csvfile)
        writer.writerow(['Title', 'Link', 'Time Ago', 'Description'])
        writer.writerows(data)

# Main function
def main():
    query = "USA"  # Change this to your desired search query
    driver = init_driver()
    page_source = extract_news(driver, query)
    data = parse_page_source(page_source)
    save_to_csv(data, 'cnn_news_results.csv')
    driver.quit()

if __name__ == '__main__':
    main()
