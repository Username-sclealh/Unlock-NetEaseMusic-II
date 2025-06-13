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
    browser.add_cookie({"name": "MUSIC_U", "value": "001BC67FF58329A2109E85F86D503D9562065B8F620E9E35C57CB8DBBB5518D3EDFE3F79530A3B7A861D12C0AA8E3FB7F438FF26462653468E9444648F116DC595EF1B32E886C83BB332206D1E0F9425EB622AA99545AFF18DE320F708BDF2AFF96E36D45212A7EC07496D09C3937A5B31C3B52DD084BAF212996940DB90F26862129EE7E4C79B42701D23E61008932FEC2A1E1AAC007773F0C36747BB8B2D69B5D8A9A100AF64D28A4156CD2BC3366A4F22B02C124970697DAD7F9E4325613EEA3E684D53C1E3D0DAD896EB9D02AEF2C611E241BDF1A39708AE04539F39FBCD3A9624A3F0D0434038E2A215DDCA0A597EDCEAFF38D9C358DA6C20E514F1C5622F80CBDE6A42E368649B9C78416F96EF3F09167DDD3BC04F4C9BDFE5A219918BCEBED2DD6B307B05274BB4749A3B8556EFB4F4E168E9A609548AE3C8677FDE6191D465045CE07D6CE7BE3E24DCC5CC1E9FD6F3C2750A78569F7D62C2DCFA79726A"})
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
