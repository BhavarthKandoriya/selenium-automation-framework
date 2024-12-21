import os

from selenium.webdriver.common.keys import Keys

from locators import home_page_elements
from pages.products_page import ProductsPage
from utilities.common_utils import get_logger
from utilities.selenium_actions import SeleniumActions


class LoginPage(SeleniumActions):
    def __init__(self, driver):
        super().__init__(driver)
        self.home_elements = home_page_elements.elements
        self.logger = get_logger(__name__)

    def enter_username_password(self, username, password):
        self.find_and_type(*self.home_elements.get('_username_input'), username)
        self.find_and_type(*self.home_elements.get('_password_input'), password)
        self.find_and_click(*self.home_elements.get('_log_in_button'))
        return ProductsPage(self.driver)

    def validate_error_message(self):
        return self.get_alert_text()