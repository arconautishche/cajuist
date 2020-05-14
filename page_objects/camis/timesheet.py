import os

from dotenv import load_dotenv
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.support.ui import WebDriverWait

from page_objects.camis.entry import Entry

class Timesheet(object):
    def __init__(self):
        print('-- 🐢 OPENING UP CAMIS 🐢 --')

        load_dotenv()
        login = os.getenv('CAMIS_LOGIN')
        pwd = os.getenv('CAMIS_PASSWORD')

        self.browser = webdriver.Chrome('selenium_drivers\\chromedriver.exe')
        self.browser.get(f'https://{login}:{pwd}@camis.cegeka.com/agresso')
        self.browser.implicitly_wait(2)

        self.__switch_to_ts_frame()
        self.__read_existing_entries()

    def close(self):
        self.browser.quit()

    def add_new_entry(self):
        add_btn_selector = '#b_s89_g89s90_buttons__newButton'
        add_btn = self.browser.find_element_by_css_selector(add_btn_selector)
        self.browser.execute_script("arguments[0].scrollIntoView();", add_btn) # sometimes the Add button may be out of view
        add_btn.click()

        new_entry = Entry.get_all_entries(self.browser)[-1]
        return new_entry

    def find_entry_by(self, workorder: str, activity: str, description: str) -> Entry:
        from_existing_entries = self.__get_existing_entry(workorder, activity, description)
        return from_existing_entries

    def save(self):
        #SAVE_BTN_SELECTOR = '#b\\$tblsysSave'
        #save_btn = browser.find_element_by_css_selector(SAVE_BTN_SELECTOR)
        #save_btn.click()
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

    def __read_existing_entries(self):
        print('Reading existing entries...')
        self.existing_entries = {}

        entries = Entry.get_all_entries(self.browser)
        for entry in entries:
            entry_attributes = (
                entry.get_workorder(), 
                entry.get_activity(), 
                entry.get_description()
            )
            self.existing_entries[entry_attributes] = entry        

    def __get_existing_entry(self, workorder: str, activity: str, description: str) -> Entry:
        if not self.existing_entries:
            return None

        entry_attributes = (workorder, activity, description)
        if entry_attributes in self.existing_entries.keys():
            return self.existing_entries[entry_attributes]

        return None
