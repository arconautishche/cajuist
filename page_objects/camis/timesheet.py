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
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.common.keys import Keys

from page_objects.camis.entry import Entry
from page_objects.camis.ms_signin import MsSignin

class Timesheet(object):
    def __init__(self, headless: bool):
        print('-- 🐢 OPENING UP CAMIS 🐢 --')
        print(f'\tHeadless: {headless}')

        load_dotenv()
        chrome_options = Options()

        self.__set_headless_options(chrome_options, headless)
        
        self.browser = webdriver.Chrome(options=chrome_options)
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
            ms_signin.start_login(os.getenv('AD_LOGIN'), os.getenv('AD_PASSWORD'))
            print('\tApprove sign-in!')

    def add_new_entry(self):
        add_btn_selector = '#b_s89_g89s90_buttons__newButton'
        add_btn = self.browser.find_element(By.CSS_SELECTOR, add_btn_selector)
        self.browser.execute_script("arguments[0].scrollIntoView();", add_btn) # sometimes the Add button may be out of view
        add_btn.click()

        new_entry = Entry.get_all_entries(self.browser)[-1]

        return new_entry

    def set_date(self, date: datetime):
        date_input_selector = '#b_s71_s84_s85_l84s85_ctl00_date_in_period_i'
        date_input = self.browser.find_element(By.CSS_SELECTOR, date_input_selector)
        date_input.send_keys(date.strftime('%m/%d/%Y'))
        date_input.send_keys(Keys.TAB)


    def find_draft_entry_by(self, workorder: str, activity: str, description: str) -> Entry:
        from_existing_entries = self.__get_existing_entry("Draft", workorder, activity, description)
        return from_existing_entries

    def save(self):
        save_btn_selector = '#b\\$tblsysSave'
        save_btn = self.browser.find_element(By.CSS_SELECTOR, save_btn_selector)
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
        if headless:
            chrome_options.add_argument("--headless=new")  # Use new headless mode
            chrome_options.add_argument("--window-size=1920x1080")
            chrome_options.add_argument("--no-sandbox")
            chrome_options.add_argument("--disable-dev-shm-usage")
            chrome_options.add_argument("--disable-gpu")
            chrome_options.add_argument("--disable-extensions")
            chrome_options.add_argument("--disable-plugins")
            chrome_options.add_argument("--disable-images")
            chrome_options.add_argument("--disable-javascript")  # Optional: disable JS for faster loading
            chrome_options.add_argument("--disable-web-security")
            chrome_options.add_argument("--allow-running-insecure-content")
            chrome_options.add_argument("--user-agent=Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36")
            
            # Set locale for consistent behavior
            try:
                locale.setlocale(locale.LC_ALL, 'nl_BE')
            except locale.Error:
                # Fallback to default locale if nl_BE is not available
                pass
