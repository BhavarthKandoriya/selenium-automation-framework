import os

from selenium.webdriver.common.keys import Keys

from locators import home_page_elements, cart_page_elements
from pages.products_page import ProductsPage
from utilities.common_utils import get_logger
from utilities.selenium_actions import SeleniumActions


class CartPage(SeleniumActions):
    def __init__(self, driver):
        super().__init__(driver)
        self.cart_elements = cart_page_elements.elements
        self.logger = get_logger(__name__)

    def place_order(self):
        self.find_and_click(*self.cart_elements.get('_place_order_button'))
        self.find_and_type(*self.cart_elements.get('_name_input'), os.getenv('CORRECT_USERNAME'))
        self.find_and_type(*self.cart_elements.get('_creditcard_input'), os.getenv('CREDIT_CARD'))
        self.find_and_click(*self.cart_elements.get('_purchase_button'))

    def get_success_message(self):
        return self.get_text(*self.cart_elements.get('_success_alert'))