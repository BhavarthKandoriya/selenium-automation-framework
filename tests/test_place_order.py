import os
import allure
from dotenv import load_dotenv
from pages.header_page import HeaderPage
from utilities.common_utils import get_logger, elk_logger
from utilities.elasticsearch_utils import ElasticSearchUtility

logger = get_logger(__name__)  # Use global logger instance
es_utility = ElasticSearchUtility(index_name="automation-logs")


@elk_logger
@allure.feature("Place Order")
@allure.story("User places an order and validates the success message")
@allure.severity(allure.severity_level.CRITICAL)
def test_place_order(driver, request):
    """Test case to place an order and validate the success message."""
    load_dotenv()  # Load environment variables from .env file

    with allure.step("Step 1: Navigate to the login page"):
        logger.info("Navigating to the login page.")
        header_page = HeaderPage(driver)
        login_page = header_page.open_login_page()

    with allure.step("Step 2: Enter username and password"):
        logger.info("Entering username and password.")
        product_page = login_page.enter_username_password(
            os.getenv('CORRECT_USERNAME'), os.getenv('CORRECT_PASSWORD')
        )

    with allure.step("Step 3: Validate logged-in username"):
        logger.info("Validating the logged-in username.")
        logged_in_username = product_page.validate_username()
        assert os.getenv('CORRECT_USERNAME') in logged_in_username, "Username validation failed."

    with allure.step("Step 4: Add product to cart"):
        logger.info("Adding product to cart.")
        product_page.add_to_cart()
        message = product_page.validate_alert_message()
        assert "Product added." in message, "Product addition message not found."

    with allure.step("Step 5: Navigate to the cart page and place the order"):
        logger.info("Navigating to the cart page and placing the order.")
        cart_page = header_page.open_cart_page()
        cart_page.place_order()

    with allure.step("Step 6: Validate the order success message"):
        logger.info("Validating the order success message.")
        success_message = cart_page.get_success_message()
        assert (
            os.getenv('AMOUNT_VERIFICATION') in success_message and
            os.getenv('CREDIT_CARD_VERIFICATION') in success_message and
            os.getenv('NAME_VERIFICATION') in success_message
        ), "Order success message validation failed."