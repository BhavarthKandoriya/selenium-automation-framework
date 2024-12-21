import os

from selenium.webdriver.common.keys import Keys

from locators import products_page_elements
from utilities.common_utils import get_logger
from utilities.selenium_actions import SeleniumActions

class ProductsPage(SeleniumActions):
    def __init__(self, driver):
        super().__init__(driver)
        self.products_page_elements = products_page_elements.elements
        self.logger = get_logger(__name__)

    def validate_username(self):
        return self.get_text(*self.products_page_elements.get('_logged_in_username'))

    def add_to_cart(self):
        self.find_and_click(*self.products_page_elements.get('_product_link'))
        self.find_and_click(*self.products_page_elements.get('_add_to_cart_link'))

    def validate_alert_message(self):
        return self.get_alert_text()