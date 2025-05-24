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
    browser.add_cookie({"name": "MUSIC_U", "value": "00ACAF5139125A533BFE07055715929A71A29CDCEA098DDD93A7996A2D26EDFF560A83B3AA3774F9EAE3F2804A559875E3192834E172EAC66D3B1799FC11A857C0AF6CCC2E3F8E3C5B776F6FF4CFB3C21AD9A3C10E38EF4FC9AAFFFD4A1C6A997A40C4DA3310C8E59590373EFDBE9F8C2ED6DE304D5ACB79DA1558E80F0A5BB9D6D366BD9D5CC927183605B2D0B999804BF1365B9865E38277550210464E24C164790EAFBBA4D6742643718177A88FC9CFF85BEF3536D6430448431B1D35B81FB6E89E1B988D7062898AD08A9254A3C6AFD869FA1E5216EFAD3E95DC26095C271C7633CDA6009DA11421A2740249C4ECCEEA241ADE2871F82DEAB2EF9E8FA0631E31AA857630C4DBB7CD90A6052884D924563CAAA0C907DFE9D0F3318EB179BAE14393F874D6E47DBCEBD2F270D6F93A6AFCEFD037CB5D917201F6A37E8F10ED7B6B2018A098CCB3F422C8FE2793506587F4AD0D3B49B2772BA131936C564CBE33"})
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
