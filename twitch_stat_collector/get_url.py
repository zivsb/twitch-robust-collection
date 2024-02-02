from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
import time
import sys


if len(sys.argv) != 3:
    print("Usage: python3 get_url.py CATEGORY ORDER")
    sys.exit(1)

# Twitch directory URL
CATEGORY = sys.argv[1]
ORDER = sys.argv[2]    
url = "https://www.twitch.tv/directory/category/" + CATEGORY

# Setup Chrome options
chrome_options = Options()
chrome_options.add_argument("--headless")
# Uncomment the next line if you want to run Chrome in headless mode
# chrome_options.add_argument("--headless")

# Initialize WebDriver
driver = webdriver.Chrome(options=chrome_options)

try:
    # Open the Twitch directory page
    driver.get(url)

    # Wait for the page elements to load
    wait = WebDriverWait(driver, 30)
    first_stream_element = wait.until(EC.presence_of_element_located((By.CSS_SELECTOR, 'div[style="order: ' + ORDER + ';"]')))

    # Extract and print the URL
    link_element = first_stream_element.find_element(By.CSS_SELECTOR, 'a[data-a-target="preview-card-image-link"]')
    stream_url = link_element.get_attribute('href')
    print(stream_url)

except Exception as e:
    print("An error occurred:", e)

finally:
    # Close the browser
    driver.quit()


