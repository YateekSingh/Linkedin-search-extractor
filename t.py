from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.by import By
from selenium.webdriver.support.wait import WebDriverWait
from selenium.common.exceptions import NoSuchElementException

import time
import openpyxl
import os

test_url = "put your search link with derised filters applied"

# Configure Chrome options
chrome_options = Options()
chrome_options.add_argument("--headless")  # Run Chrome in headless mode (without opening a browser window)
chrome_options.add_argument("--no-sandbox")
chrome_options.add_argument("--disable-dev-shm-usage")

# Initialize Chrome driver
driver = webdriver.Chrome(options=chrome_options)
driver.get("https://linkedin.com")
driver.set_window_size(1920, 1080)  # Set a larger window size to prevent crashes due to minimized windows

wait = WebDriverWait(driver, 5)

username_field = wait.until(EC.presence_of_element_located((By.XPATH, "//*[@id='session_key']")))
password_field = wait.until(EC.presence_of_element_located((By.XPATH, "//*[@id='session_password']")))

username_field.send_keys("singhyateek420@gmail.com")
password_field.send_keys("Iyateek@786")

submit = wait.until(EC.element_to_be_clickable((By.XPATH, "//button[@type='submit']"))).click()

driver.get(test_url)

links = []

while True:
    # Scroll to the bottom of the page
    driver.execute_script("window.scrollTo(0,document.body.scrollHeight);")
    # Wait for the page to load new search results
    time.sleep(3)

    # Scrape links of current search results
    results = driver.find_elements(By.XPATH, "//li[contains(@class, 'reusable-search__result-container')]")

    for result in results:
        link_element = result.find_element(By.XPATH, ".//a[contains(@class, 'app-aware-link')]")
        link = link_element.get_attribute("href")
        links.append(link)
        print(f"Extracted link: {link}")

        file_path = "links.xlsx"  # Excel file path
        if not os.path.exists(file_path):
            workbook = openpyxl.Workbook()
            sheet = workbook.active
            sheet.append(["Links"])
        else:
            workbook = openpyxl.load_workbook(file_path)
            sheet = workbook.active

        sheet.append([link])
        workbook.save(file_path)
        workbook.close()

    try:
        # Check if the "Next" button is disabled
        next_button = wait.until(EC.presence_of_element_located((By.XPATH, "//button[@aria-label='Next']")))
        is_disabled = next_button.get_attribute("disabled")

        if is_disabled == "true":
            break
        else:
            # Click the "Next" button to load more search results
            driver.execute_script("arguments[0].click();", next_button)
            # Wait for the next page to load
            wait.until(EC.staleness_of(results[0]))
            # Scroll to the bottom of the page again
            driver.execute_script("window.scrollTo(0,document.body.scrollHeight);")
            # Wait for the page to load new search results
            time.sleep(3)
    except NoSuchElementException:
        break

# Print the extracted links
print("Total links extracted:", len(links))
for link in links:
    print(link)

# Close the driver when finished
driver.quit()
