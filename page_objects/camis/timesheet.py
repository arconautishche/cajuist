import os

from dotenv import load_dotenv
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.support.ui import WebDriverWait

from page_objects.camis.entry import Entry

class Timesheet(object):
    def __init__(self):
        load_dotenv()
        login = os.getenv('LOGIN')
        pwd = os.getenv('PASSWORD')

        self.cache = {}

        self.browser = webdriver.Chrome('selenium_drivers\\chromedriver.exe')
        self.browser.get(f'https://{login}:{pwd}@camis.cegeka.com/agresso')
        self.browser.implicitly_wait(2)

        self.__switch_to_ts_frame()

    def close(self):
        self.browser.quit()

    def add_new_entry(self):
        add_btn_selector = '#b_s89_g89s90_buttons__newButton'
        add_btn = self.browser.find_element_by_css_selector(add_btn_selector)
        self.browser.execute_script("arguments[0].scrollIntoView();", add_btn) # sometimes the Add button may be out of view
        add_btn.click()

        new_entry = Entry.get_all_entries(self.browser)[-1]
        return new_entry

    def all_entries(self):
        entries = Entry.get_all_entries(self.browser)
        self.__refresh_cache(entries)
        return entries

    def find_entry_by(self, workorder: str, activity: str, description: str) -> Entry:
        from_cache = self.__get_entry_from_cache(workorder, activity, description)
        if from_cache is None:
            all_entries = Entry.get_all_entries(self.browser)
            self.__refresh_cache(all_entries)        
            from_cache = self.__get_entry_from_cache(workorder, activity, description)

        return from_cache

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

    def __refresh_cache(self, entries):
        print('Refreshing the cache...')
        all_ids = list(e.entry_id for e in self.cache.values())
        for entry in entries:
            if entry.entry_id not in all_ids:
                self.__add_entry_to_cache(entry)

    def __add_entry_to_cache(self, entry: Entry):
        entry_attributes = (
            entry.get_workorder(), 
            entry.get_activity(), 
            entry.get_description()
        )
        self.cache[entry_attributes] = entry

    def __get_entry_from_cache(self, workorder: str, activity: str, description: str) -> Entry:
        if not self.cache:
            return None

        entry_attributes = (workorder, activity, description)
        if entry_attributes in self.cache.keys():
            return self.cache[entry_attributes]

        return None
