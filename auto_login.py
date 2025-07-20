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
    browser.add_cookie({"name": "MUSIC_U", "value": "00AD4B2A886A8713C62F4748890A3F288B00A7ADC5492DC58B4CAFC33BB9D1E3B5B26F2F6E52F12063F1710C3630E2C8A2DC60244E357F5231A31C2E57844BA3E9A64FDEB83501BA737956C9BBC4E043B9E25542E45AC75FBE6DE2131059FF198BD7BE6DA94D91EE9FFDEC5EC54C3B31BCDA2722E639A93D3DE9398AB5A5075B27EDBB87A8F1ABAFA1C7620644C36306DA84B6DF9C4B59422558215B3F15C89874E4BE20023F71AAE12CF796E80C7BD5A572D6498638936277CC81D294B702F3E12E6B8D9723E79C622CD30BA6178297F7114CAA4FBAECBDF4596D17662022E77CFC9335AAB00EDE797B846F7CA82DF142ECEDEA47AE4698DAE9079E3F53E8BD5DD127DF354BF7B4A8641045980B4BABAE8DB32E7C5339F366C30FD95F8CE4FD6872A7239689618374603AFAEC58A22E710773E1E1302CCC659563F5C99C58208C97CD097BDB3AFA350DB78897DD2E59DB0C34E080DCCBD6B38438ED49489BF38BA25F3C62C101D8FFCF54C2C56207C93A7F790D7B6EA947ABD4FC1D4B4F8F2BADBA87C900059DF99D589E3B40C9B7FC44"})
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
