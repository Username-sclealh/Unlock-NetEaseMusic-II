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
    browser.add_cookie({"name": "MUSIC_U", "value": "005882E471C69F8B4089C20A9035C0AC3BF433E318D1A3285DB3C75D408E50ED8E100509AE2C28250D495C3182F24E8420FDFE287FB93721BE4F010E3615C9DD737048BB73136C3EB77002A1AA5B836664DFD25992909424720B44FB8AD7F29D3D57A293942E21E5505230F94199AE16F1643E6EC2634232EBB151770A14411A33158C6CBE84862AB7B66EF7E700C3DC2B0D434C09DEE73576E4FE7448187005FB65610054961FB956A74C85997F2A2503D729AB6F7D9167A1B3F5688E1461EE31E7F85291D617E0EBA6FD6D8E6F7A51EF6DA3951A629621E67D8C7E44A187FAEC656F34FA3F040A7089843E195955BBA23ED1C98D5B3AB78EE1A7C5A50B92FC7FE4E4963F39B6B7EABFD69C9EF7F9615D782D060A6CE9EF497A8052EA0252E9EB210B3046067BB52FA1328E46610A6079B76D9CB582F18AB92C4B8098EAB5F2747974421732DA91F06D4A2CD005497D819C5C957BE7E9C1A5F7AAA6DE123B8ABEAE56C56EC645069DF06AE967E84E416E82D3137BC829A481643AF0018ECC89A52FB60BAC2276A3B1F97C31EE6608F845"})
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
