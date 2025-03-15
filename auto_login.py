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
    browser.add_cookie({"name": "MUSIC_U", "value": "00DBBE5DBA58CEC5A8B049ECD4470490A22447E98E955F6B884EC2BB85249A15C190C7BC3A2861D84BC19B6CD652BF4D0B0B00422E7CC90A6DCAF2611857CD7879F35342BE14559E292F8430526BD6EF16E2188145CEC5F21C9A25106E68ADD0B9D067EFEFB2FD4C0D003CD31CF9C377867AC27E8D72720D73D317C2E774EF6ABB991BB8BB42E5E36FB67A8B98BD2826C16905C4711BBA673963341D25DBF72A029C49EA8A2CFC140E53A1F51C05FC7D45ABA2A677A4C1993807134DBCC86E950364872BE4DECC9870D192166FFEFE5AC90607BA8A174A4788800DFFD30C8261182CB8660EC50C3DB03997A5C91D450F2012F386E0927A82B8B7D775BFAC87BDBD732BBA0CE619CF622924CD56A8965CD1C96C143B11808A16AD823EB1E830FB9A6EEF746EC3232DD355080B2EEAA717F439856E3F1D9F812D044DBFE5D6869CC6BD3825AADF0A649C4BAA48B0BE63869CF659D1064B4B026D9861A423BDE07EF9"})
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
