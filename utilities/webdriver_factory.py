import os
from selenium import webdriver
from selenium.webdriver.chrome.service import Service as ChromeService
from selenium.webdriver.firefox.service import Service as FirefoxService
from selenium.webdriver.edge.service import Service as EdgeService
from selenium.webdriver.chrome.options import Options as ChromeOptions
from selenium.webdriver.firefox.options import Options as FirefoxOptions
from selenium.webdriver.edge.options import Options as EdgeOptions
from dotenv import load_dotenv

class WebDriverFactory:
    def __init__(self):
        # Load environment variables from .env file
        load_dotenv()
        # Get the browser type from environment variables
        self.browser = os.getenv('BROWSER').lower()

    def get_webdriver(self):
        """Get the appropriate WebDriver based on the browser specified in the .env file."""
        if self.browser == 'chrome':
            return self._get_chrome_driver()
        elif self.browser == 'firefox':
            return self._get_firefox_driver()
        elif self.browser == 'edge':
            return self._get_edge_driver()
        else:
            raise ValueError(f"Unsupported browser: {self.browser}")

    def _get_chrome_driver(self):
        """Create a Chrome WebDriver instance."""
        chrome_options = ChromeOptions()
        # Set Chrome options if needed
        chrome_options.add_argument('--headless')  # Example option
        # You may specify the path to the ChromeDriver executable if not in PATH
        #chrome_service = ChromeService(executable_path='/path/to/chromedriver')
        return webdriver.Chrome()

    def _get_firefox_driver(self):
        """Create a Firefox WebDriver instance."""
        firefox_options = FirefoxOptions()
        # Set Firefox options if needed
        firefox_options.add_argument('--headless')  # Example option
        # You may specify the path to the GeckoDriver executable if not in PATH
        firefox_service = FirefoxService(executable_path='/path/to/geckodriver')
        return webdriver.Firefox(service=firefox_service, options=firefox_options)

    def _get_edge_driver(self):
        """Create an Edge WebDriver instance."""
        edge_options = EdgeOptions()
        # Set Edge options if needed
        edge_options.add_argument('--headless')  # Example option
        # You may specify the path to the EdgeDriver executable if not in PATH
        edge_service = EdgeService(executable_path='/path/to/edgedriver')
        return webdriver.Edge(service=edge_service, options=edge_options)