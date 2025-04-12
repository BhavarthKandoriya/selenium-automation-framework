import logging
import os

import pytest
from dotenv import load_dotenv

from utilities.common_utils import preserve_allure_history
from utilities.webdriver_factory import WebDriverFactory

logger = logging.getLogger(__name__)

'''def pytest_sessionstart(session):
    """Called before any tests are executed."""
    preserve_allure_history()
    print("Allure history has been preserved.")'''


def pytest_addoption(parser):
    parser.addoption(
        "--env",
        action="store",
        default="dev",
        help="Environment to run tests against (e.g., dev, qa)"
    )

@pytest.fixture(scope="function")
def setup_driver(request):
    # Create an instance of WebDriverFactory
    factory = WebDriverFactory()
    # Get the WebDriver instance
    driver = factory.get_webdriver()
    # Set the driver in the request.cls attribute so it's accessible in the test class
    request.cls.driver = driver

    # Yield to allow the test class to execute
    yield

    # Teardown: Quit the driver
    driver.quit()


@pytest.fixture(scope="function", params=["chrome", "firefox"])
def driver(request):
    """Fixture to set up and tear down the WebDriver."""
    # Create an instance of WebDriverFactory
    # Get the browser parameter
    browser = request.param
    # Override the BROWSER environment variable
    import os
    os.environ["BROWSER"] = browser
    factory = WebDriverFactory()
    # Get the WebDriver instance
    driver = factory.get_webdriver()

    # Yield the driver to the test function
    yield driver

    # Teardown: Quit the driver
    driver.quit()

@pytest.fixture(scope="session", autouse=True)
def load_env_file(request):
    env_name = request.config.getoption("--env")
    env_file = f".env.{env_name}"

    if os.path.exists(env_file):
        load_dotenv(dotenv_path=env_file)
        print(f"[INFO] Loaded environment variables from {env_file}")
    else:
        raise FileNotFoundError(f"[ERROR] Environment file '{env_file}' not found.")
