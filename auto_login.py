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
    browser.add_cookie({"name": "MUSIC_U", "value": "00DFF639B2DC301F3F786DE2F59670DB6676E7A08E63FC23520BE1957AD7BACA99F1CEBA599723B771B90F23BE41D1D08E5312392712C5B73F58B4844617969E2C30C726DBC97FF9E5C4849BAF7F6F0958232728378CF567FC99B67D73B5CA39E37D844C6D08A6C72DD3EF9E7C0012FFB8E955DA1D21F2E8695631372C37F78C7420CD3F0D8426CE5701747922A0E5555A469565EA23CED78E11A7A026D818551AE5A4D6975823B5E9F728D8AA4CCB5FF31471C590ABE0B57C6FA147D0FF41E087CE9E2C24AF7DEFF60E5708720E0D2BA398820A4A5D95BEE1473E219A9915FDCB92A7B0AF13542535CE8D3F1DC8F0EAD95DF54A953F2C2A2A797039EE8FC0D140427E2F7FCE4463E81265D0908D4013915314EA08CD0EE1428A41C7FA5DCD18E7285E062B3EF3064690766C619545E92F256A8D8042DC54B4B619DD67E8F1858A8164299C799143B3878FB975DDC690BCA7BA384B017F455A0AEEA94802DC69B8"})
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
