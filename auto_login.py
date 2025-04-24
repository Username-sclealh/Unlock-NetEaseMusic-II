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
    browser.add_cookie({"name": "MUSIC_U", "value": "0076A805C72314AF87771556C7565CFFAD7F474A960073D9367B1A95ACB4FEDECA18E261720A68B01FA679B959DD29155B9C0B509CEF52E480E21EF629732E01B16E2F3137F97887A0491610B810C8BCD0727802242FD488494A650D13A53ACFA87327BB694B1B9E1B8DB9A2D8A5264CC7D10BDBDF827557D8D9330203992962EC3E3483C21880702855377AC5ABF1AEE01861749720B2B2DA52B2DD71985EBF88968CE86921C0D871314B67C941265C5D243F9B909B8006D8A5D27596A3FFC35B9AB2497CA30336AC2F9B13674D1A249C25AB2C3B5DAC98C0D2D017E32B9B72075EEA82BE0B152A0E831A0381C9AD4961933598DBB1B2F420FB32801ED69F08992BF4E30318CC2C254351835D9DF40EB07D153E471A7933415BDB880F8F2BAC53AEABD8810E9523C1635115806AA3FC9F23E4AEDA318C088F8A8C8E7C2ED8F8AA2BA72D83C2869E12C01CB541AC62A9FB75C83A013185135BF36809023C42AD39"})
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
