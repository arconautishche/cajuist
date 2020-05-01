import time

from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.remote.webdriver import WebDriver
from selenium.webdriver.remote.webelement import WebElement

class Entry:
    CONTAINER = (By.CSS_SELECTOR, '#b_s89_g89s90')
    ENTRY_ROW = (By.XPATH, 'tbody/tr')

    XPATH_TO_INPUT = '//tbody/tr[1]/td[1]//input[1]'
    TIMECODE_INPUT = (By.XPATH, f'td[5]{XPATH_TO_INPUT}')
    WORKORDER_INPUT = (By.XPATH, f'td[6]{XPATH_TO_INPUT}')
    ACTIVITY_INPUT = (By.XPATH, f'td[7]{XPATH_TO_INPUT}')
    DESCRIPTION_INPUT = (By.XPATH, f'td[8]{XPATH_TO_INPUT}')

    def __init__(self, browser: WebDriver, entry_tr: WebElement):
        self.browser = browser
        self.entry_tr = entry_tr 
        self.entry_id = self.entry_tr.get_attribute('id')

    def get_timecode(self):
        return self.__get_entry_attribute(Entry.TIMECODE_INPUT)

    def get_workorder(self):
        return self.__get_entry_attribute(Entry.WORKORDER_INPUT)

    def get_activity(self):
        return self.__get_entry_attribute(Entry.ACTIVITY_INPUT)

    def get_description(self):
        return self.__get_entry_attribute(Entry.DESCRIPTION_INPUT)

    def set_workorder(self, workorder: str):
        self.__set_entry_attribute(Entry.WORKORDER_INPUT, workorder)

    def set_activity(self, activity: str):
        self.__set_entry_attribute(Entry.ACTIVITY_INPUT, activity)

    def set_description(self, description: str):
        self.__set_entry_attribute(Entry.DESCRIPTION_INPUT, description)

    def set_hours(self, day, hours):
        DAY_INPUT = (By.XPATH, f'td[{day+10}]{Entry.XPATH_TO_INPUT}')
        self.__set_entry_hours(DAY_INPUT, hours)

    @staticmethod
    def get_all_entries(browser: WebDriver):
        container = Entry.__container(browser)
        entries = list(
            [Entry(browser, tr) for tr in container.find_elements(*Entry.ENTRY_ROW)[:-2]]
        )

        return entries

    ### PRIVATE ###
    @staticmethod
    def __container(browser):
        entries_container = browser.find_element(*Entry.CONTAINER)
        return entries_container

    def __fresh(self):
        # CAMIS recreates the whole <table> all the time
        container = Entry.__container(self.browser)
        entry_tr = container.find_element_by_id(self.entry_id)

        return entry_tr

    def __get_entry_attribute(self, selector: tuple):
        attribute = self.__fresh().find_element(*selector)
        return attribute.get_attribute('value')

    def __set_entry_attribute(self, selector: tuple, value: str):
        attribute_input = self.__fresh().find_element(*selector)
        attribute_input.clear()
        attribute_input.send_keys(value)
        attribute_input.send_keys(Keys.TAB)
        time.sleep(1)

    def __set_entry_hours(self, selector: tuple, value: str):
        hour_input = self.__fresh().find_element(*selector)
        hour_input.click()
        
        hour_input.send_keys(Keys.CONTROL + 'a')
        hour_input.send_keys(Keys.DELETE)

        hour_input.send_keys(value)
        hour_input.send_keys(Keys.TAB)
        time.sleep(1)
