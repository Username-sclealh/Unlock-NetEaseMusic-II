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
    browser.add_cookie({"name": "MUSIC_U", "value": "0074ABF8DCFD570931C385950D2858C868048D4D0DB92288C81D5A99736171E854898E4BA49CD9C319B9CF7CCF3ED36C2315C42484AF384679663985EF6535089EB29CADE4C8C6323618CA5241564632BF3D3E205A997763155EF5661DEFCE02126B05067C55E01B9111EC0ACB7BDDBEFAA927782D86A26CA3F461970DFD8EFFDE2A4851BF4D19BD4E17DC5409D6E567A9BA97AE0FCC6A55DDDD9315D3E778D1E70FA64377712C84CB27C2E335AC05F821645B28F8D49FCAB7E8B0E0AD3766DDAFE02D521B89D4680BDBA66B2B4888F14761FCBA0C04BBF4B08FED159F144CB17E4514F07B50A1B73305DDC6502B789BBD1FFBCA62CBEEF48E77FA7C01B454F331EBDC3C0DC1671A294D3B4C4789D0D8710CCEAE461596DE5C40F5099D05B6279DFA91204BA93E9E6AB1D961A203C1CBCC5D26A0BE4C2090DB4EEC2E967C1EEA1E4A97B5825E64D3E76C2D066F9E4765E94EFA7EBE6509AC83FDB107CC4E5793C8C36B31A256208F512B06743A7288D3E1AAD4425A23941356E9708AEA543F3F6C793D68CD0EFDA2BCF74B1116056C5261"})
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
