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
    browser.add_cookie({"name": "MUSIC_U", "value": "0007B08C17656D60977A4515EDF674C07FECA5462E8D97C60CC7385D9EDE5587F586D59E95E75F1BB4C38E7ADACE9AF1FC1D434431E358E1FAA6BBB226DB81B51C4B16B9AF765B2E1A92D2E8EABEB10D671A8416AB945FC94E11168157170A87FD7CCFFA3EFAB3859684EB6AC07714DD18986A9A5EA554A3BC6665B0612D9F7EA8301BE310B5FF387A12BBDADF3490A8574E6E9D07B8DBFC15AE2A1E47216440B2367CB1CF6613B52DD3112BA0F23ECB48525216253F4AC3A546BEB6C05C3A953BE63A082563D7DCEAE1A4F31961CBE0123ED668E9B84D3537ABA33ECE7B777343244C23C6B541703F1BE529E26E3D52D0FA35D0BB7BDB472BE704CF2B0A2A742D1B785CFBD8EB7F6A947417431A28A482DFD608204EB38AF52C7B081E3AAABD1CA67259A9C716AF5CD74E95A8629C3AE9D7EAAD260ECFB58DD68DC98A8E7ACD2423E5C8E73B40EE94D7CE9915CBC73045CAC70486D78B571CD67A3913919A28BF4327306EC011437BDDA2EEE004056004CC5344091C90B82554D6E50E7922387471AC57A287EE22E5A468EADF9C09499A"})
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
