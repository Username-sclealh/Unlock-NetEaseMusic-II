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
    browser.add_cookie({"name": "MUSIC_U", "value": "0053F736D61B8AC456826BBE0D06B4F625463873F72A14243089CB2F01D73451F69F57FE6AD21D425082D60E35AE4687C0AC6B613AB54ED33FBDAA3A738BBCCCF9EC5990FCCF5B9BB2E152DD851A24980FE5F64D4D53A447A934B5FE5A03139D9F0CE290AA426ABE797137637C68DFB52B3404CF59571E1C3714FBC8857759B6E8B82F70A547474A4911891A3BAA6B435B9D6C9B2581FFA06C88019AF9045357D9CF2E3B45985DAF01471183EA646B03B80C740FAACC7A73CBDFFB9B15F8F65512ED4BB49E357942759C0DC1C0FBEFB5DE484356A2220F2FE4E714E96ED9A5B009CDC433C29E4AEF895FA121E6A44966823541D72959FB49225BE281445CFF4E256D4925D68BCC0ED7D5DF6383CD3582AEAA2599D0BE86AF76181AD4D0293E08D51CE597B9E4EE61241E995C8BE5E14D247879495B1A18062FC9C993EE1D37833E628C3680BF873E75C4612E74BCA69A4BE93805471BB3842FDB8F234BB149974B"})
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
