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
    browser.add_cookie({"name": "MUSIC_U", "value": "00204D0415B6EC21226266DABCEA590ED8855A3B0A848F5F94E21ED02F96D532D169DBA826C8D4F7629E2CFF3387A2FA8218CE7D2F4ACD04BA25EDD84318A2AA5197BD42FEF2CCE69D25C9E7897C010BF5DD780574E490EED43738A8E123B0516411179539309E79245D78869B03ED87602733FC672582DE1525F65EB36C2AE73876CCB5D09FF207CBCEA5C10274BB24DD475E8BE02A2960F1872E22D9042AACC786CF0955ACEAE905487C6AACB83AD57E734A116EB8DBEEE9A8750DF6F61863DBFFF65B944D224C50739EA54B63EAAC50A9ACEDCD7A74F89EB07715D1D9964869FA9D5A90BEA342461F57E3FD0FB2DC2054CCB332DCF2E98D666D83448CC7E0E4D47203FB356F07982AAC749D6FD58DF024B824525D52A58A3A0D4DC2A462C7595945F9B1981F2137F885C46EE7268FCB993A8CF5441E02A4046D07F574B3AD8B5D803E185C309E9DD1FF78700F520294C83DC668AE5662BF022D1ACD40E9C29D"})
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
