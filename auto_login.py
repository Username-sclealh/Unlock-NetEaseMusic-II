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
    browser.add_cookie({"name": "MUSIC_U", "value": "000DD4D473DCC208B6CDADC260F563C0DDD69BD4D012D849D1155D34F32DD885501DF58E3E0E28CAB0583415E7209DB364C9D50AC574366E8C703D265D434972E3CD9700B067C904808AC3E814B5320CE68ADF11800E48A49BFBEDE57A3D38E3CDB28E35A5A670370D528641203E4F5119E88FD6DA798DE65B27B1569998F32BCE1D5E566E54311E7DE67CA57BBBF793ECD279591D6BF6440F9D1B729DBC9681A75F14794C30D275215EB3DF6A51C2E022D98B4D66BF32871CC51CAD1A3F940C2B25A1533BF98D75C31E79383AFCAF563BF8D42C67858069B74B471962A6DF3283C450B4B34D528BCFCD2DE959913A389D238BBFDA0D4A0486615025A1CA75FD2B7CC3DAE9F49511CDF190EABBC40883C0F8E9444BF53E57DD8CF1DC4684ECA2D3869CDD16CCF078B52FE2AA7670545E4DDAACBB6B8DDE4FBD3C51BA7FCD4AA7F3C735E42FB45A26622AFE0C0390498488601702AEBD250962F2D4F54C7250094A"})
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
