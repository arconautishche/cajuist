import os
from dotenv import load_dotenv
load_dotenv()
login = os.getenv('LOGIN')
pwd = os.getenv('PASSWORD')

from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC

browser = webdriver.Chrome('C:\\Users\\antoniar\\Documents\\Code\\cajuist\\selenium_drivers\\chromedriver.exe')
browser.get(f'https://{login}:{pwd}@camis.cegeka.com/agresso')
browser.implicitly_wait(2)

# CAMIS looooves iframes...
WebDriverWait(browser, 30).until(
    EC.frame_to_be_available_and_switch_to_it((By.CSS_SELECTOR, 'iframe'))
)

WebDriverWait(browser, 30).until(
    EC.frame_to_be_available_and_switch_to_it((By.CSS_SELECTOR, 'frame'))
)

def new_ts_entry():
    ADD_BTN_SELECTOR = '#b_s89_g89s90_buttons__newButton'
    add_btn = browser.find_element_by_css_selector(ADD_BTN_SELECTOR)
    add_btn.click()

new_ts_entry()
new_ts_entry()

TS_TABLE_SELECTOR = '#b_s89_g89s90'
ts_table = browser.find_element_by_css_selector(TS_TABLE_SELECTOR)
ts_rows = ts_table.find_elements_by_xpath('tbody/tr')[:-2]

for row in ts_rows:
    row.screenshot(f'ts_row_{row.get_attribute("id")}_before.png')

browser.quit()

