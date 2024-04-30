from selenium import webdriver
from selenium.webdriver.common.keys import Keys
from bs4 import BeautifulSoup
import csv
import time


def init_driver():
    driver = webdriver.Chrome()
    return driver


def extract_news(driver, query):
    url = f"https://news.google.com/search?q={query}&hl=en-US&gl=US&ceid=US%3Aen"
    driver.get(url)
    time.sleep(2)  # Wait for page to load
    page_source = driver.page_source
    return page_source

def parse_page_source(page_source):
	soup = BeautifulSoup(page_source, 'html.parser')
	articles = soup.find_all('article')[:100]  # Limiting to top 100 results

	data = []
	for article in articles:
		title = article.find('a', class_='JtKRv').text
		link = article.find('a', class_='JtKRv')['href']
		time_ago = article.find('time', class_='hvbAAd').text

		data.append([title, link, time_ago, 'NA'])

	return data

# Function to save data to CSV
def save_to_csv(data, filename):
    with open(filename, 'w', newline='', encoding='utf-8') as csvfile:
        writer = csv.writer(csvfile)
        writer.writerow(['Title', 'Link', 'Time Ago', 'Authors'])
        writer.writerows(data)

# Main function
def main():
    query = "cnn"  # Change this to your desired search query
    driver = init_driver()
    page_source = extract_news(driver, query)
    data = parse_page_source(page_source)
    save_to_csv(data, 'SeleniumGoogleResults.csv')
    driver.quit()

if __name__ == '__main__':
    main()
