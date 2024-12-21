from selenium.webdriver.support.wait import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from utilities.common_utils import get_logger

class SeleniumActions:
    """Wrapper around Selenium WebDriver actions to add logging and error handling."""

    def __init__(self, driver):
        self.driver = driver
        self.logger = get_logger(__name__)  # Reuse the global logger

    def open_url(self, url):
        """Opens a specified URL in the browser."""
        try:
            self.logger.info(f"Opening URL: {url}")
            self.driver.get(url)
            self.logger.info(f"Successfully opened URL: {url}")
        except Exception as e:
            self._log_and_raise(f"Failed to open URL: {url}", e)

    def find_and_click(self, by, value, timeout=10):
        """Finds an element by locator and clicks it. Timeout is optional (default: 10s)."""
        try:
            self.logger.info(f"Attempting to click element: {by}={value}")
            element = self._wait_for_element(by, value, timeout)
            element.click()
            self.logger.info(f"Successfully clicked element: {by}={value}")
        except Exception as e:
            self._log_and_raise(f"Failed to click element: {by}={value}", e)

    def find_and_type(self, by, value, text, timeout=10):
        """Finds an element by locator and sends text to it. Timeout is optional (default: 10s)."""
        try:
            self.logger.info(f"Typing '{text}' into element: {by}={value}")
            element = self._wait_for_element(by, value, timeout)
            element.send_keys(text)
            self.logger.info(f"Successfully typed '{text}' into element: {by}={value}")
        except Exception as e:
            self._log_and_raise(f"Failed to type into element: {by}={value}", e)

    def get_text(self, by, value, timeout=10):
        """Retrieves the text from the specified element. Timeout is optional (default: 10s)."""
        try:
            self.logger.info(f"Getting text from element: {by}={value}")
            element = self._wait_for_element(by, value, timeout)
            text = element.text
            self.logger.info(f"Retrieved text from element: {by}={value} | Text: '{text}'")
            return text
        except Exception as e:
            self._log_and_raise(f"Failed to get text from element: {by}={value}", e)

    def get_alert_text(self, timeout=10):
        """Retrieves and accepts the alert text. Timeout is optional (default: 10s)."""
        try:
            self.logger.info("Waiting for alert to be present.")
            WebDriverWait(self.driver, timeout).until(EC.alert_is_present())
            alert = self.driver.switch_to.alert
            alert_text = alert.text
            self.logger.info(f"Alert text: '{alert_text}'")
            alert.accept()
            self.logger.info("Alert accepted successfully.")
            return alert_text
        except Exception as e:
            self._log_and_raise("Failed to retrieve or accept alert", e)

    def _wait_for_element(self, by, value, timeout=10):
        """Waits for the visibility of an element and returns it. Timeout is optional (default: 10s)."""
        try:
            self.logger.debug(f"Waiting for element: {by}={value} (Timeout: {timeout}s)")
            element = WebDriverWait(self.driver, timeout).until(
                EC.visibility_of_element_located((by, value))
            )
            self.logger.debug(f"Element located: {by}={value}")
            return element
        except Exception as e:
            self._log_and_raise(f"Timeout while waiting for element: {by}={value}", e)

    def _log_and_raise(self, message, exception):
        """Logs an error message and raises the exception."""
        self.logger.error(f"{message} | Exception: {str(exception)}", exc_info=True)
        raise exception  # Re-raise for test handling
