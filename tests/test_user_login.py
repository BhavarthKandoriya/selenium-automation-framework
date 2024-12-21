import os

import allure

from pages.header_page import HeaderPage
from utilities.common_utils import get_logger, log_and_ingest_failure, elk_logger

logger = get_logger(__name__)  # Use the global logger instance


@elk_logger
@allure.feature("User Login")
@allure.story("Login with Correct Credentials")
def test_user_login_with_correct_credentials(driver, request):
    """Test user login with correct credentials."""
    # Step 1: Navigate to the login page
    logger.info("Navigating to the login page.")
    with allure.step("Navigate to the login page"):
        header_page = HeaderPage(driver)
        login_page = header_page.open_login_page()

    # Step 2: Enter correct username and password
    logger.info("Entering correct username and password.")
    with allure.step("Enter correct username and password"):
        product_page = login_page.enter_username_password(
            os.getenv('CORRECT_USERNAME'), os.getenv('CORRECT_PASSWORD')
        )

    # Step 3: Validate logged-in username
    logger.info("Validating the logged-in username.")
    with allure.step("Validate logged-in username"):
        logged_in_username = product_page.validate_username()
        assert os.getenv('CORRECT_USERNAME') in logged_in_username, "Username validation failed."


@elk_logger
@allure.feature("User Login")
@allure.story("Login with Incorrect Password")
def test_user_login_with_incorrect_password(driver, request):
    """Test user login with incorrect password."""
    # Step 1: Navigate to the login page
    logger.info("Navigating to the login page.")
    with allure.step("Navigate to the login page"):
        header_page = HeaderPage(driver)
        login_page = header_page.open_login_page()

    # Step 2: Enter correct username with incorrect password
    with allure.step("Enter correct username and incorrect password"):
        logger.info("Entering correct username with incorrect password.")
        product_page = login_page.enter_username_password(
            os.getenv('CORRECT_USERNAME'), os.getenv('INCORRECT_PASSWORD')
        )

    # Step 3: Validate error message
    with allure.step("Validate error message for incorrect password"):
        logger.info("Validating the error message for incorrect password.")
        error_message = login_page.validate_error_message()
        assert os.getenv('WRONG_PASSWORD_ERROR_MESSAGE') in error_message, \
            "Incorrect password error message validation failed."


@elk_logger
@allure.feature("User Login")
@allure.story("Login with Incorrect Username")
def test_user_login_with_incorrect_username(driver, request):
    """Test user login with incorrect username."""
    # Step 1: Navigate to the login page
    logger.info("Navigating to the login page.")
    with allure.step("Navigate to the login page"):
        header_page = HeaderPage(driver)
        login_page = header_page.open_login_page()

    # Step 2: Enter incorrect username with correct password
    logger.info("Entering incorrect username with correct password.")
    with allure.step("Enter incorrect username and correct password"):
        product_page = login_page.enter_username_password(
            os.getenv('INCORRECT_USERNAME'), os.getenv('CORRECT_PASSWORD')
        )

    # Step 3: Validate error message
    logger.info("Validating the error message for incorrect username.")
    with allure.step("Validate error message for incorrect username"):
        error_message = login_page.validate_error_message()
        assert os.getenv('WRONG_USERNAME_ERROR_MESSAGE') in error_message, \
            "Incorrect username error message validation failed."