import os
import locale
import time

from datetime import datetime
from dotenv import load_dotenv

from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.chrome.options import Options

from page_objects.camis.entry import Entry
from page_objects.camis.ms_signin import MsSignin

class Timesheet(object):
    def __init__(self, headless: bool):
        print('-- 🐢 OPENING UP CAMIS 🐢 --')
        print(f'\tHeadless: {headless}')

        load_dotenv()
        chrome_options = Options()

        self.__set_headless_options(chrome_options, headless)
        
        self.browser = webdriver.Chrome('selenium_drivers\\chromedriver.exe', options=chrome_options)
        self.browser.get('https://camis.cegeka.com/agresso')
        self.browser.implicitly_wait(2)

        self.__sign_in()

        self.__switch_to_ts_frame()
        self.__read_all_existing_entries()

    def close(self):
        self.browser.quit()

    def __sign_in(self):
        ms_signin = MsSignin(self.browser)
        if (ms_signin.is_visible()):
            ms_signin.start_login(os.getenv('AD_LOGIN'))
            print('\tApprove sign-in!')

    def add_new_entry(self):
        add_btn_selector = '#b_s89_g89s90_buttons__newButton'
        add_btn = self.browser.find_element_by_css_selector(add_btn_selector)
        self.browser.execute_script("arguments[0].scrollIntoView();", add_btn) # sometimes the Add button may be out of view
        add_btn.click()

        new_entry = Entry.get_all_entries(self.browser)[-1]

        return new_entry

    def find_draft_entry_by(self, workorder: str, activity: str, description: str) -> Entry:
        from_existing_entries = self.__get_existing_entry("Draft", workorder, activity, description)
        return from_existing_entries

    def save(self):
        save_btn_selector = '#b\\$tblsysSave'
        save_btn = self.browser.find_element_by_css_selector(save_btn_selector)
        save_btn.click()

        self.__wait_for_success_popup()

    ### PRIVATE ###
    def __switch_to_ts_frame(self):
        # CAMIS looooves iframes...
        WebDriverWait(self.browser, 30).until(
            EC.frame_to_be_available_and_switch_to_it((By.CSS_SELECTOR, 'iframe'))
        )

        WebDriverWait(self.browser, 30).until(
            EC.frame_to_be_available_and_switch_to_it((By.CSS_SELECTOR, 'frame'))
        )

    def __read_all_existing_entries(self):
        print('Reading all existing entries...')
        self.existing_entries = {}

        entries = Entry.get_all_entries(self.browser)
        for entry in entries:
            entry_attributes = (
                entry.get_status(),
                entry.get_workorder(), 
                entry.get_activity(), 
                entry.get_description()
            )
            self.existing_entries[entry_attributes] = entry        

    def __get_existing_entry(self, status: str, workorder: str, activity: str, description: str) -> Entry:
        if not self.existing_entries:
            return None

        entry_attributes = (status, workorder, activity, description)
        if entry_attributes in self.existing_entries.keys():
            return self.existing_entries[entry_attributes]

        return None

    def __wait_for_success_popup(self):
        time.sleep(5)
        # this doesn't seem to work...
        # WebDriverWait(self.browser, 30).until(
        #    EC.visibility_of_element_located((By.CSS_SELECTOR, 'div.u4-messageoverlay-success'))
        #)

    def __set_headless_options(self, chrome_options: Options, headless: bool):
        return
        
        # DOESN'T REALLY WORK YET
        if (headless):
            chrome_options.add_argument("--headless")
            chrome_options.add_argument("--window-size=1920x1080")
            locale.setlocale(locale.LC_ALL, 'nl_BE')
