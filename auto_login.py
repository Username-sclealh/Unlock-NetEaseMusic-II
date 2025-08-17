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
    browser.add_cookie({"name": "MUSIC_U", "value": "00DD4F11920FD5AEAD9C022E212A119C6385F7104D0D999D0C6DEEDFDD4895C71527011734A7E4D3EFDF7361061F09FE154CC6D45612C5B0AAD013CCAFE7518EDECEC4D9BAF575548F06979207589B374ACFE0A556C3FD5993C928ED6F3D7786B822D67FEC4D1C7787A96D4DED03E30EC3BA86550E07C103C53EBCF508DE57D7F69625592162D66B042F9337FD9DF10D61747A291D11AC234046328C646FC1F5735BFD12F7D2E4ED1C4DDF8F3D7322FFA145FE0BB6194A792151573785E106452BB48C5B62C03564587FCFE216D84A0BB827F283A09979FCAEC64674618D62E9F122002BF3C57A087D5B1F313892D5868946D4CEC03993C2D3D17D3304627A0585F0551BF5490E5CE384A15835826910F0749B419DE97610BB50AD2191C21C2AFD2D8D1AF9E91CC028F4A8D55D0C33E0EC80B8E0306475285FFDB1A7268B517A64BAF0982AF07AA3C95A2E0DCE0508F9D45DC959A5C9814E6DA550C2D449CD345547923B95A6B0DE009AA2E775E4563A9F61A0241328AC418DF33ADC9DDCE3371F33061719EC0AD368DBE3B107A3D7E11B"})
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
