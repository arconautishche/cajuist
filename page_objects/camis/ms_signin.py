import os
import time
import pyotp
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.common.by import By
from selenium.webdriver.remote.webdriver import WebDriver
from selenium.webdriver.remote.webelement import WebElement
from selenium.common.exceptions import NoSuchElementException
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC


class MsSignin:

    def __init__(self, browser: WebDriver):
        self.browser = browser
        self.login_field_selector = "#i0116"
        self.password_field_selector = "#i0118"
        self.submit_button_selector = "#idSIButton9"
        self.totp_field_selector = "#idTxtBx_SAOTCC_OTC"

    def is_visible(self):
        try:
            self.browser.find_element(By.CSS_SELECTOR, self.login_field_selector)
        except NoSuchElementException:
            return False

        return True

    def start_login(self, ad_login: str, ad_password: str):
        login_field = self.browser.find_element(By.CSS_SELECTOR, self.login_field_selector)
        login_field.send_keys(ad_login)
        login_field.send_keys(Keys.ENTER)
        time.sleep(1)
        
        # Wait for password field to appear and enter password
        try:
            password_field = WebDriverWait(self.browser, 10).until(
                EC.presence_of_element_located((By.CSS_SELECTOR, self.password_field_selector))
            )
            
            if ad_password:
                password_field.send_keys(ad_password)
                password_field.send_keys(Keys.ENTER)                
                print('\tPassword entered automatically')
                
                # Wait for TOTP field to appear and enter TOTP code
                time.sleep(1)
                self.__handle_totp()
            else:
                print('\tAD_PASSWORD not found in environment variables. Please enter password manually.')
        except Exception as e:
            print(f'\tCould not find password field or enter password automatically: {e}')
            print('\tPlease enter password manually.')
    
    def __handle_totp(self):
        """Handle TOTP code entry if required"""
        try:
            # Wait for TOTP field to appear
            totp_field = WebDriverWait(self.browser, 10).until(
                EC.presence_of_element_located((By.CSS_SELECTOR, self.totp_field_selector))
            )
            
            # Get TOTP secret from environment variable
            totp_secret = os.getenv('TOTP_SECRET')
            if totp_secret:
                # Generate current TOTP code
                totp = pyotp.TOTP(totp_secret)
                current_code = totp.now()
                
                # Enter the TOTP code
                totp_field.send_keys(current_code)
                totp_field.send_keys(Keys.ENTER)
                print('\tTOTP code entered automatically')
            else:
                print('\tTOTP_SECRET not found in environment variables. Please enter TOTP code manually.')
        except Exception as e:
            print(f'\tTOTP field not found or could not enter TOTP automatically: {e}')
            print('\tPlease enter TOTP code manually if required.')

