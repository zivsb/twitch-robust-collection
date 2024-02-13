from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.common.by import By
from selenium.webdriver.common.desired_capabilities import DesiredCapabilities
from selenium.common.exceptions import NoSuchElementException
import time
import json
import csv
import sys



# Constants
if len(sys.argv) != 6:
    print("Usage: python3 script.py TWITCH_URL CATEGORY_NAME ITERATION CURRENT_DIR TIMESTAMP")
    sys.exit(1)

TWITCH_URL = sys.argv[1]
CATEGORY_NAME = sys.argv[2]  # Now included but not used directly in file naming
ITERATION = sys.argv[3]  # Now included but not used directly in file naming
CURRENT_DIR = sys.argv[4]
TIMESTAMP = sys.argv[5]


SCRIPT_PATHS = ['./browser_scripts/twitch_analyze.js', 
                './browser_scripts/twitch_unmute.js', 
                './browser_scripts/twitch_low_latency.js',
                './browser_scripts/twitch_normal_latency.js']

CSV_PATH = f'{CURRENT_DIR}/data_iter{ITERATION}_{TIMESTAMP}.csv'
HTTP_LOGS_PATH = f'{CURRENT_DIR}/httplogs_iter{ITERATION}_{TIMESTAMP}.json'

# Create CSV file if it doesn't exist
with open(CSV_PATH, 'w', newline='') as file:
    fieldnames = [
        "timeStamp", "Video Resolution", "Display Resolution", "FPS", "Skipped Frames",
        "Buffer Size", "Latency To Broadcaster", "Latency Mode", "Playback Bitrate",
        "Backend Version", "Serving ID", "Codecs", "Play Session ID", "Protocol", "isRebuffering", "inAd"
    ]
    writer = csv.DictWriter(file, fieldnames=fieldnames)
    writer.writeheader()

# Function to read JavaScript files
def read_script(file_path):
    with open(file_path, 'r') as file:
        return file.read()

# Load JavaScript scripts
js_analyze, js_unmute, js_low_latency, js_normal_latency = map(read_script, SCRIPT_PATHS)
http_logs = []

# Function to configure Chrome options
def configure_chrome_options():
    options = Options()
    options.add_argument("--headless")
    options.set_capability('goog:loggingPrefs', {'browser': 'ALL', 'performance': 'ALL'})
    options.page_load_strategy = 'eager'
    options.add_experimental_option('perfLoggingPrefs', {
        'enableNetwork': True,
    })
    return options

# Function to process performance logs
def process_performance_log(driver):
    logs = driver.get_log('performance')
    for entry in logs:
        log_json = json.loads(entry['message'])['message']
        if 'Network.responseReceived' in log_json['method']:
            http_logs.append(log_json)

# Function to get and process new logs
def get_new_logs(driver, last_timestamp):
    new_logs = [entry for entry in driver.get_log('browser') if entry['timestamp'] > last_timestamp]
    return new_logs

# Function to process and print logs
def process_logs(driver, last_timestamp):
    new_logs = get_new_logs(driver, last_timestamp)
    if new_logs:
        for log in new_logs:
            if "PRIVATE_DATALOG" not in log['message']:
                continue
                # print(log['message'], '\n')
            else:
                try:
                    # print("PRIVATE_DATALOG\n")
                    # Extract the JSON string from the log message
                    json_str = log['message'].split('PRIVATE_DATALOG',1)[1].strip()
                    json_str = json_str.replace('\\"', '"')
                    json_str = json_str.replace('}"', '}')
                    json_data = json.loads(json_str)

                    write_to_csv(json_data)
                except Exception as e:
                    print(f"Error parsing JSON!!: {e}\n")

        return new_logs[-1]['timestamp']
    return last_timestamp

# Define the expected field names
fieldnames = ['timeStamp', 'Video Resolution', 'Display Resolution', 'FPS', 'Skipped Frames', 'Buffer Size', 
              'Latency To Broadcaster', 'Latency Mode', 'Playback Bitrate', 'Backend Version', 'Serving ID', 
              'Codecs', 'Play Session ID', 'Protocol', 'isRebuffering', 'inAd']

def write_to_csv(data):
    with open(CSV_PATH, 'a', newline='') as file:
        writer = csv.DictWriter(file, fieldnames=fieldnames)

        # Ensure each field has a value, even if it's an empty string
        csv_data = {field: data.get(field, '') for field in fieldnames}

        # Write the row to the CSV file
        writer.writerow(csv_data)


# Function to wait for an element to be present
def wait_for_element(driver, css_selector, timeout=45):
    end_time = time.time() + timeout
    print(f"Waiting for element with selector {css_selector}...")
    while True:
        try:
            element = driver.find_elements(By.CSS_SELECTOR, css_selector)
            if element:
                return element[0]
            elif time.time() > end_time:
                raise TimeoutError(f"Element with selector {css_selector} not found in {timeout} seconds")
        except NoSuchElementException:
            pass
        time.sleep(0.05)  # Wait 50ms before trying again


def print_progress(iteration, total, prefix='Progress:', suffix='Complete', decimals=1, length=50, fill='█', printEnd="\r"):
    """
    Call in a loop to create terminal progress bar
    @params:
        iteration   - Required  : current iteration (Int)
        total       - Required  : total iterations (Int)
        prefix      - Optional  : prefix string (Str)
        suffix      - Optional  : suffix string (Str)
        decimals    - Optional  : positive number of decimals in percent complete (Int)
        length      - Optional  : character length of bar (Int)
        fill        - Optional  : bar fill character (Str)
        printEnd    - Optional  : end character (e.g. "\r", "\r\n") (Str)
    """
    percent = ("{0:." + str(decimals) + "f}").format(100 * (iteration / float(total)))
    filledLength = int(length * iteration // total)
    bar = fill * filledLength + '-' * (length - filledLength)
    print(f'\r{prefix} |{bar}| {percent}% {suffix}', end=printEnd)
    # Print New Line on Complete
    if iteration == total: 
        print()

# Initialize WebDriver
options = configure_chrome_options()
driver = webdriver.Chrome(options=options)


driver.execute_script(js_analyze)

# Open the Twitch stream
print("Loading page...")
driver.get(TWITCH_URL)
print("Page partially loaded, waiting for key element to enter")

last_log_timestamp = 0

# Wait for and interact with page to unlock unmute
# See the link below for reasoning:
    #  https://developer.chrome.com/blog/autoplay/
temp_interact_element = wait_for_element(driver, '[aria-label="About Panel"]')
print("Page loaded")
temp_interact_element.click()
print("Clicked on the about panel")
last_log_timestamp = process_logs(driver, last_log_timestamp)

# Make sure the stream isn't age restricted
try:
    age_restricted_element = driver.find_element(By.CSS_SELECTOR, 'div[data-a-target="content-classification-gate-overlay"]')
    print("Age restricted content detected | SKIPPING STREAM")
    driver.quit()
    sys.exit(1)
except NoSuchElementException:
    pass


# Unmute and set low latency
for script in [js_unmute, js_low_latency]:
# for script in [js_unmute, js_normal_latency]:
    driver.execute_script(script)
    last_log_timestamp = process_logs(driver, last_log_timestamp)

print("Going into data collection loop...")

# Execute the JavaScript every 100ms for 3 minutes
total_iterations = 1800
print_progress(0, total_iterations)
for i in range(1800):
    driver.execute_script(js_analyze)
    time.sleep(0.1)
    last_log_timestamp = process_logs(driver, last_log_timestamp)
    print_progress(i+1, total_iterations)

# Process performance logs for HTTP logs
process_performance_log(driver)

# Save the HTTP logs to a file
with open(HTTP_LOGS_PATH, 'w') as log_file:
    json.dump(http_logs, log_file, indent=4)

# Close the browser
driver.quit()
