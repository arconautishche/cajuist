from selenium.webdriver.common.keys import Keys
from selenium.webdriver.remote.webdriver import WebDriver
from selenium.webdriver.remote.webelement import WebElement
from selenium.common.exceptions import NoSuchElementException


class MsSignin:

    def __init__(self, browser: WebDriver):
        self.browser = browser
        self.login_field_selector = "#i0116"

    def is_visible(self):
        try:
            self.browser.find_element_by_css_selector(self.login_field_selector)
        except NoSuchElementException:
            return False

        return True

    def start_login(self, ad_login: str):
        login_field = self.browser.find_element_by_css_selector(self.login_field_selector)
        login_field.send_keys(ad_login)
        login_field.send_keys(Keys.ENTER)

