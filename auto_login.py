# coding: utf-8

import os
import time
import logging
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from webdriver_manager.chrome import ChromeDriverManager
from retrying import retry

# Configure logging
logging.basicConfig(level=logging.INFO, format='[%(levelname)s] %(asctime)s %(message)s')

@retry(wait_random_min=5000, wait_random_max=10000, stop_max_attempt_number=3)
def enter_iframe(browser):
    logging.info("Enter login iframe")
    time.sleep(5)  # 给 iframe 额外时间加载
    try:
        iframe = WebDriverWait(browser, 10).until(
            EC.presence_of_element_located((By.XPATH, "//*[starts-with(@id,'x-URS-iframe')]")
        ))
        browser.switch_to.frame(iframe)
        logging.info("Switched to login iframe")
    except Exception as e:
        logging.error(f"Failed to enter iframe: {e}")
        browser.save_screenshot("debug_iframe.png")  # 记录截图
        raise
    return browser

@retry(wait_random_min=1000, wait_random_max=3000, stop_max_attempt_number=5)
def extension_login():
    chrome_options = webdriver.ChromeOptions()

    logging.info("Load Chrome extension NetEaseMusicWorldPlus")
    chrome_options.add_extension('NetEaseMusicWorldPlus.crx')

    logging.info("Initializing Chrome WebDriver")
    try:
        service = Service(ChromeDriverManager().install())  # Auto-download correct chromedriver
        browser = webdriver.Chrome(service=service, options=chrome_options)
    except Exception as e:
        logging.error(f"Failed to initialize ChromeDriver: {e}")
        return

    # Set global implicit wait
    browser.implicitly_wait(20)

    browser.get('https://music.163.com')

    # Inject Cookie to skip login
    logging.info("Injecting Cookie to skip login")
    browser.add_cookie({"name": "MUSIC_U", "value": "00985E1918DFFCE3F7A87AC8CAD49DBB034262C276C91DCA7837ED1EFEDBAA6AE2407502BFCC3B81F2B65F276F3B8317F074C0C01EC3011CA4FBAF28DC0AA67623F801105F83803735ECD97E444F052A18EA5BBB3895546B32ECF058650E86A030E7989208420DBAB70306D96F701F7595F9B8BCFACFFB77BB50D9F4A2482DA0A7F4BC53E0B1C2B34BCD15BE224FAFF4B4D016955DD31BC5CD77FA86B0F0F3A7A9BACB9C7F8369C8464795482312EB3AD8F6AE8DC872825D5AD146884C4E61CFC500A03743DD2A558D209F0B02539FB2CA31CBCFD6D9D921FD478CEB9216AD630B435ABB42648CB10607AF5D5959F006AB9994646983D7F778631E1A48496E6F9DF9ACC5157C1D09CDA1E16BD9968664A2B0AA3C5FA38C1B389442CA91BACBEC196E5FD3A1374179CEAF7262B6921BC4DE2F4274CA5E931829D15EB3201BBD2C10C98DF1CDAEA646C3798CBD631A7BB2C6ADEB459F6661BFE1CF66558A4A94A30579877E39630E3A805BA423ABD344EBF6B327C82886FA09372B76A876CC159B642332B64831D87CE85CDB2670F342984D"})
    browser.refresh()
    time.sleep(5)  # Wait for the page to refresh
    logging.info("Cookie login successful")

    # Confirm login is successful
    logging.info("Unlock finished")

    time.sleep(10)
    browser.quit()


if __name__ == '__main__':
    try:
        extension_login()
    except Exception as e:
        logging.error(f"Failed to execute login script: {e}")
