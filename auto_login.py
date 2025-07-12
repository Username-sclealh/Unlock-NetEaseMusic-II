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
    browser.add_cookie({"name": "MUSIC_U", "value": "008BF5FEF2B1BBF89037D90207905B2155D68B814BF324EA652D00DE67C8E084FE0B304D0A3F09C89C2941F4261E6D5F70C6CCE7864D9392DFF71936E5F9408548CDAA4CABEFE34E41E08213A01C5956045748E6AE595184A2B808C9A1054088B712C30F262E739BE0B32EF43B1E1609A426111B86F2253128752FABE71D43039B5956CE371900C8CA1791A94E92C45F4479BC88BEF135F844250E19938DCE4E3D497BCC803EDC74E5311BCE9B737A53E73F30EBB0F12B637714286554DEB82C96448AAB4EF2F7C621C485DB09B0E19EC21AFF7A52588E38CFAA8781AEEB0A8B1CD9898C1510C92055B1BD76D27B5E45D64AE83A453125455CF73DCEE2F6EAFD3C453A33B69FF73ADA6655F0A984D248B2E8501408257306E597642FFAC104FC93B218AB0BF96DE1D0AACD8CA53AAE1506EB2999F3920DE45DF1C50C32C11A1D0C47AD3E5CADC95DD53B75DE2717D890B5ECA77ECA621E896436A0FB4A3EFA102B"})
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
