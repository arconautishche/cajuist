import time

from selenium.webdriver.common.keys import Keys
from selenium.webdriver.remote.webdriver import WebDriver
from selenium.webdriver.remote.webelement import WebElement


class Entry:
    '''
    Allows interacting with a Timesheet Entry rows
    '''
    STATUS_INDEX = 4
    TIMECODE_INDEX = 5
    WORKORDER_INDEX = 6
    ACTIVITY_INDEX = 7
    DESCRIPTION_INDEX = 8

    def __init__(self, browser: WebDriver, entry_tr: WebElement):
        self.browser = browser
        self.entry_tr = entry_tr
        self.entry_id = self.entry_tr.get_attribute('id')

    def get_status(self):
        return self.__get_entry_attribute(Entry.STATUS_INDEX)

    def get_timecode(self):
        return self.__get_entry_attribute(Entry.TIMECODE_INDEX)

    def get_workorder(self):
        return self.__get_entry_attribute(Entry.WORKORDER_INDEX)

    def get_activity(self):
        return self.__get_entry_attribute(Entry.ACTIVITY_INDEX)

    def get_description(self):
        return self.__get_entry_attribute(Entry.DESCRIPTION_INDEX)

    def set_workorder(self, workorder: str):
        self.__set_entry_attribute(Entry.WORKORDER_INDEX, workorder)

    def set_activity(self, activity: str):
        self.__set_entry_attribute(Entry.ACTIVITY_INDEX, activity)

    def set_description(self, description: str):
        self.__set_entry_attribute(Entry.DESCRIPTION_INDEX, description)

    def set_hours(self, day, hours):
        self.__set_entry_hours(day+10, hours)

    def select(self):
        refreshed_elem = self.__fresh()

        # sometimes the row may be out of view
        self.browser.execute_script("arguments[0].scrollIntoView();", refreshed_elem)
        
        refreshed_elem.click()
        time.sleep(1)

    @staticmethod
    def get_all_entries(browser: WebDriver):
        container = Entry.__container(browser)
        entries = list(
            map(
                lambda tr: Entry(browser, tr),
                container.find_elements_by_xpath('tbody/tr')[:-2]
            )
        )

        return entries

    ### PRIVATE ###
    @staticmethod
    def __container(browser):
        entries_container = browser.find_element_by_css_selector('#b_s89_g89s90')
        return entries_container

    def __fresh(self):
        # CAMIS recreates the whole <table> all the time
        container = Entry.__container(self.browser)
        entry_tr = container.find_element_by_id(self.entry_id)

        return entry_tr

    def __find_text(self, cell_index: int):
        xpath = f'td[{cell_index}]/div[1][not(*)]'
        text_elem = self.__fresh().find_element_by_xpath(xpath)
        return text_elem

    def __find_input(self, cell_index: int):
        xpath = f'td[{cell_index}]//tbody/tr[1]/td[1]//input[1]'
        input_elem = self.__fresh().find_element_by_xpath(xpath)
        return input_elem

    def __get_entry_attribute(self, cell_index: int):
        try:
            attribute = self.__find_text(cell_index)
            return attribute.text
        except:
            if self.__is_cell_empty(cell_index):
                return ''

            attribute = self.__find_input(cell_index)
            return attribute.get_attribute('value')

    def __set_entry_attribute(self, cell_index: int, value: str):
        attribute_input = self.__find_input(cell_index)

        attribute_input.clear()
        attribute_input.send_keys(value)
        attribute_input.send_keys(Keys.TAB)
        time.sleep(1)

    def __set_entry_hours(self, cell_index: int, value: str):
        hour_input = self.__find_input(cell_index)
        hour_input.click()

        hour_input.send_keys(Keys.CONTROL + 'a')
        hour_input.send_keys(Keys.DELETE)

        hour_input.send_keys(str(value))
        hour_input.send_keys(Keys.TAB)
        time.sleep(1)

    def __is_cell_empty(self, cell_index: int):
        xpath = f'td[{cell_index}][not(*)]'
        try:
            self.__fresh().find_element_by_xpath(xpath)
            return True
        except:
            return False
