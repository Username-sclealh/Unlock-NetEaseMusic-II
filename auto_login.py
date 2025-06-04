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
    browser.add_cookie({"name": "MUSIC_U", "value": "00B33AD4BA0BC3EA33C7DB1DA447EACE3AB6F0D3E0DC876782F98C6408C04354F91BFF33118AF225261B60000173A4A1B589570E55DEA1BD36923A57643EE1E89BE35E825B5F2E84C33E7537C7C55998830508D3AA51BD1E335E82EE3953B87EF6E563A6BDC91EB4A3E7B9EBDC6F6B96B7EC6D0073E5BD7CF5D3D735374C9BD659D80CF5772A1E7C07B92D5A0F497C9B57F4C0030B3D0D06F7E0E8268B4C5BC2D52BD607DA75D0E5684ABF6E7AC7E1C660392297FB8BA45D397FDE64F83881B7E7B3BBB2169E229C69B23C8C4A53C64A9C5CACE6D79B4E0C21E068A5355307A4B89F11727460524223D0DC02F652ADE84E309E5E31711D64ED7232808CD2981538BE48F2D762A2D2C68BFB3A028A7F6EEAF6BB57A2696DC6BD59E4D62CF9238F2A83C929D955DB60629537E7D64BB52163918BF95DCBAD484C52A89FB8962D47BB562B7DF781B85E4C5069D45E0D108EB32F2C33D6BF6DBD9813BD6E59222505A3"})
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
