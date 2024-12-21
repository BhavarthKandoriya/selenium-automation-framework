import os

from selenium.webdriver.common.keys import Keys

from locators import signup_page_elements
from pages.products_page import ProductsPage
from utilities.common_utils import get_logger
from utilities.selenium_actions import SeleniumActions


class SignUpPage(SeleniumActions):
    def __init__(self, driver):
        super().__init__(driver)
        self.sign_up_elements = signup_page_elements.elements
        self.logger = get_logger(__name__)

    def enter_username(self, username):
        self.find_and_type(*self.sign_up_elements.get('_username_input'), username)

    def enter_password(self, password):
        self.find_and_type(*self.sign_up_elements.get('_password_input'), password)

    def click_signup_button(self):
        self.find_and_click(*self.sign_up_elements.get('_sign_up_button'))

    def validate_error_message(self):
        return self.get_alert_text()