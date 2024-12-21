import os

from selenium.webdriver.common.keys import Keys

from locators import home_page_elements, header_page_elements
from pages.cart_page import CartPage
from pages.login_page import LoginPage
from pages.signup_page import SignUpPage
from pages.products_page import ProductsPage
from utilities.common_utils import get_logger
from utilities.selenium_actions import SeleniumActions

class HeaderPage(SeleniumActions):
    def __init__(self, driver):
        super().__init__(driver)
        self.open_url(os.getenv('BASE_URL'))
        self.header_elements = header_page_elements.elements
        self.logger = get_logger(__name__)

    def open_login_page(self):
        self.find_and_click(*self.header_elements.get('_log_in_link'))
        self.logger.info("Successfully clicked")
        return LoginPage(self.driver)

    def open_signup_page(self):
        self.find_and_click(*self.header_elements.get('_sign_up_link'))
        self.logger.info("Successfully clicked")
        return SignUpPage(self.driver)

    def open_cart_page(self):
        self.find_and_click(*self.header_elements.get('_cart_link'))
        self.logger.info("Successfully clicked")
        return CartPage(self.driver)