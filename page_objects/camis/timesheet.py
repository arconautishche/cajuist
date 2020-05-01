import os

from dotenv import load_dotenv
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.support.ui import WebDriverWait

class Timesheet:
    

    def __init__(self):
        load_dotenv()
        login = os.getenv('LOGIN')
        pwd = os.getenv('PASSWORD')

        self.browser = webdriver.Chrome('selenium_drivers\\chromedriver.exe')
        self.browser.get(f'https://{login}:{pwd}@camis.cegeka.com/agresso')
        self.browser.implicitly_wait(2)

        self.__switch_to_ts_frame()

    def close(self):
        self.browser.quit()

    def add_new_entry(self):
        ADD_BTN_SELECTOR = '#b_s89_g89s90_buttons__newButton'
        add_btn = self.browser.find_element_by_css_selector(ADD_BTN_SELECTOR)
        add_btn.click()

    def all_entries(self):
        pass

    def find_entry_by(self, workorder, activity, description):
        pass

    ### PRIVATE ###
    def __switch_to_ts_frame(self):
        # CAMIS looooves iframes...
        WebDriverWait(self.browser, 30).until(
            EC.frame_to_be_available_and_switch_to_it((By.CSS_SELECTOR, 'iframe'))
        )

        WebDriverWait(self.browser, 30).until(
            EC.frame_to_be_available_and_switch_to_it((By.CSS_SELECTOR, 'frame'))
        )
