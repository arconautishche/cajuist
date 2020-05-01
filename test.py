import os
import time

from dotenv import load_dotenv
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.support.ui import WebDriverWait

load_dotenv()
login = os.getenv('LOGIN')
pwd = os.getenv('PASSWORD')


browser = webdriver.Chrome('C:\\Users\\antoniar\\Documents\\Code\\cajuist\\selenium_drivers\\chromedriver.exe')
browser.get(f'https://{login}:{pwd}@camis.cegeka.com/agresso')
browser.implicitly_wait(2)

from ts_row import TimesheetEntryRow as row

new_ts_entry()

workorder_input = row.get_last(browser).find_element_by_xpath('td[6]//tbody/tr[1]/td[1]//input[1]')
workorder_input.send_keys('PZ--001.001')
workorder_input.send_keys(Keys.TAB)
time.sleep(1)

activity_input = row.get_last(browser).find_element_by_xpath('td[7]//tbody/tr[1]/td[1]//input[1]')

descr_input = row.get_last(browser).find_element_by_xpath('td[8]//tbody/tr[1]/td[1]//input[1]')
descr_input.clear()
descr_input.send_keys('Scrum')
descr_input.send_keys(Keys.TAB)
time.sleep(1)

mo_input = row.get_last().find_element_by_xpath('td[11]//tbody/tr[1]/td[1]//input[1]')
mo_input.click()
mo_input.send_keys('0.5')
mo_input.send_keys(Keys.TAB)
time.sleep(1)

SAVE_BTN_SELECTOR = '#b\\$tblsysSave'
save_btn = browser.find_element_by_css_selector(SAVE_BTN_SELECTOR)
save_btn.click()

browser.quit()
