from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.common.by import By
import time

# URL of the Twitch stream
ookla_url = 'https://www.speedtest.net/'

# Configure ChromeOptions
options = Options()

# comment out this line to see the chromedriver
options.add_argument("--headless")

options.set_capability('goog:loggingPrefs', {'browser': 'ALL'})

# Instantiate the Chrome WebDriver with options
driver = webdriver.Chrome(options=options)

print("loading page...")

driver.get(ookla_url)

print("page loaded")

# Find the 'Go' button by its class name and click it
start_test_button = driver.find_element(By.CLASS_NAME, 'js-start-test')
start_test_button.click()

print("Starting test...")

# Periodically check the download speed value
while True:
    # Find the download speed element
    download_speed_element = driver.find_element(By.CLASS_NAME, 'download-speed')

    # Get the text (value) of the download speed element
    download_speed_value = download_speed_element.text

    # Check if the value is populated
    if download_speed_value and download_speed_value != '—':
        print(f"Download Speed: {download_speed_value} Mbps")
        break

    # Wait for 200 milliseconds before checking again
    time.sleep(0.2)

driver.quit()