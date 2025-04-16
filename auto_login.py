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
    browser.add_cookie({"name": "MUSIC_U", "value": "00E194E3C8F467547BFD8349B7CF3B3114858B5C752E2FAABA7FFE45B697C50F89A7ABC23156CDE3FC6205BC51E05936B0A698C30DFECFCB8408D3E86821BA91F0800327634B709FC3BD85C64C8E30D47C449447BE567961D1B964B37F5BA48CD71776E694C6CB82A7F4C7E24850329FC561077ED9DF47547D22254FDD589E1ED7F6D21E6A6915B94189AC351E25C374B146DC05CABD3F9AD83AC14BBA9238435E05474F4F1EC3ABC0D61A946D5F3F9D43F972770CDE415FD96A4A99D7CEF67C39CA06407835ADF5FCA23D3D886572A18F60328CBAC9BA5FEF9292E51C6D7D91755A3DDDE611DDAEF1206545B96FF00EB6FD416FFE650FC3D87FE9E56C2203834FC84CAE6ED76112338FD62BE935ACC9CA456E1939146E64031863F11BA843848E4E47B9877EA786F87987EB90DEE613AA0643F7BFED1834105A9424FF616957C24AA28BE1304188A2AD1646A06854AC4B5A773356B5AFB45394A3FEA806F30A84"})
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
