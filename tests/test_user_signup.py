import os
import allure
from pages.header_page import HeaderPage
from utilities.common_utils import get_logger, elk_logger

logger = get_logger(__name__)

@elk_logger
@allure.feature("User Signup")
@allure.story("Signup without username")
@allure.severity(allure.severity_level.CRITICAL)
def test_user_signup_without_username(driver, request):
    """Test signup without providing a username."""
    with allure.step("Step 1: Navigate to the signup page"):
        header_page = HeaderPage(driver)
        sign_up_page = header_page.open_signup_page()

    with allure.step("Step 2: Enter a username and submit the signup form"):
        sign_up_page.enter_username(os.getenv('CORRECT_USERNAME'))
        sign_up_page.click_signup_button()

    with allure.step("Step 3: Reopen signup page and validate error message"):
        sign_up_page = header_page.open_signup_page()
        error_message = sign_up_page.validate_error_message()
        allure.attach(error_message, name="Error Message", attachment_type=allure.attachment_type.TEXT)
        assert error_message == os.getenv('SIGNUP_ERROR_MESSAGE'), "Error message validation failed."


@elk_logger
@allure.feature("User Signup")
@allure.story("Signup without password")
@allure.severity(allure.severity_level.CRITICAL)
def test_user_login_without_password(driver, request):
    """Test signup without providing a password."""
    with allure.step("Step 1: Navigate to the signup page"):
        header_page = HeaderPage(driver)
        sign_up_page = header_page.open_signup_page()

    with allure.step("Step 2: Enter a password and submit the signup form"):
        sign_up_page.enter_password(os.getenv('CORRECT_PASSWORD'))
        sign_up_page.click_signup_button()

    with allure.step("Step 3: Validate error message"):
        error_message = sign_up_page.validate_error_message()
        assert error_message == os.getenv('SIGNUP_ERROR_MESSAGE'), "Error message validation failed."