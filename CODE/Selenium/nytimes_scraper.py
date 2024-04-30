# Selenium libraries
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.common.exceptions import TimeoutException, NoSuchElementException
from selenium import webdriver

# Other libraries
import os
import time
import datetime
import pandas as pd
import numpy as np

start_date = datetime.datetime.strptime("01-01-2018", "%d-%m-%Y")  # start date query
end_date = datetime.datetime.strptime("01-02-2018", "%d-%m-%Y")  # end date query

date_range = pd.date_range(start_date, end_date)  # Create date range

# Generate URLs for each date
urls = [
    f"https://www.nytimes.com/search?dropmab=false&endDate={date.strftime('%Y-%m-%d')}&query=&sections=U.S.%7Cnyt%3A%2F%2Fsection%2Fa34d3d6c-c77f-5931-b951-241b4e28681c&sort=best&startDate={date.strftime('%Y-%m-%d')}&types=article"
    for date in date_range
]

# Open the browser outside the loop
chrome_options = Options()
# chrome_options.add_argument("--headless")
browser = webdriver.Chrome(options=chrome_options)
# browser.maximize_window()
links = pd.DataFrame(columns=["url", "text", "date"])

def scroll_page():
    try:
        while True:
            button_element = browser.find_element(By.XPATH, '//*[@id="site-content"]/div/div[2]/div[2]/div/button')
            if button_element:
                button_element.click()  # Click button to load more content
                time.sleep(np.random.uniform(2, 6))  # Wait for content to load
    except NoSuchElementException:
        pass

def collect(date):
    try:
        link_element = browser.find_element(By.XPATH, '//*[@id="site-content"]/div/div[2]/div/ol/li[1]/div/div/div/a')
        link_text = link_element.text
        if "PRINT EDITION" in link_text:
            url = link_element.get_attribute("href")
            links.loc[len(links)] = [url, link_text, date]
    except NoSuchElementException:
        pass

print("Starting Time:", datetime.datetime.now())
for i, url in enumerate(urls):
    try:
        browser.get(url)
        scroll_page()
        collect(date_range[i].strftime('%Y-%m-%d'))
        print(f"{i+1} out of {len(urls)}", end="\r")
    except Exception as e:
        print(f"Error processing URL {i+1}: {e}")

# Close the browser after processing all URLs
browser.quit()

links.to_csv("SeleniumNYtimeResults.csv", index=False)
print("End Time:", datetime.datetime.now())
os.system("echo 'I am done collecting urls'")
