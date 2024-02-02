import time
from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.chrome.options import Options

# Create an instance of ChromeOptions
chrome_options = Options()

# Set the desired capabilities through ChromeOptions
chrome_options.add_experimental_option('w3c', False)

# Network conditions
network_conditions = {
    "offline": False,
    "latency": 5,  # Additional latency (ms)
    "download_throughput": 500 * 1024,  # Max download speed (bytes per second)
    "upload_throughput": 500 * 1024   # Max upload speed (bytes per second)
}

# Specify the path to chromedriver executable
service = Service('/path/to/chromedriver')

# Instantiate the Chrome WebDriver with the options
driver = webdriver.Chrome(service=service, options=chrome_options)

# Set the network conditions
driver.execute_cdp_cmd("Network.emulateNetworkConditions", network_conditions)

# Navigate to a website
driver.get("http://example.com")

time.sleep(600)

# Close the browser
driver.quit()

