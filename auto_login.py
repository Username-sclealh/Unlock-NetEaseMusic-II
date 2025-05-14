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
    browser.add_cookie({"name": "MUSIC_U", "value": "00EE8469D56C593BCBC20F5DC5EC39F6D6DD5F9EFC6490BCF66A0B7C01313965C42DC8AFBAE2A0C70BDF49DDA37D30AB881464791869ACCD5DA5149295B3A69B5CE2DB1FCE4A02A998341E79C0B9887569E1CA02633D15867A4A39E9A1B9943AB504D6BFD19C30FA66037050C548D175A8233CB36FAF3AD665D6D5390E8353AEBAF3DE4B50167EB109ECCAECE282EE131953AC3F6954713B65178CDDE54CFC73FE1EC95A0D4DF0068C35655C8018B2455A68E80BE25B194EF05686F65FDBEBFCDD10C42965313FB013F917BD6236BF94F9983D24F5A60EA3E6358BD5A49D2A00456CB807ED2AE9502B10213C1FD9A526F03CBF6F2373D146F875DB5708666A2B88B790E7CECCC6E8F5AFBF9021BA0476D565B1224E7EB641FC62B8F9407818506CE0723599C307F00D6FCA22E713564FF85E93B955D3C56ACC438D528A58A4538FACAE40282A02D250B4B509C30A31743B9A04AF907B009AB585E6A1EFBF589AAE"})
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
