import logging
from functools import wraps
from logging.handlers import RotatingFileHandler
import os
import allure
import shutil
from utilities.elasticsearch_utils import ElasticSearchUtility

def get_logger(name, log_level=logging.INFO):
    """Sets up logging for the framework."""
    log_formatter = logging.Formatter(
        '%(asctime)s - %(name)s - %(levelname)s - %(message)s [%(filename)s:%(lineno)d]'
    )

    log_file = "app.log"  # Store logs in a dedicated folder
    handler = RotatingFileHandler(log_file, maxBytes=5 * 1024 * 1024, backupCount=3)  # 5MB max size, 3 backups
    handler.setFormatter(log_formatter)

    logger = logging.getLogger(name)  # Root logger
    logger.setLevel(logging.DEBUG)  # Log everything (can change to INFO/ERROR in production)
    logger.addHandler(handler)

    # Optional: Log uncaught exceptions
    def handle_exception(exc_type, exc_value, exc_traceback):
        if not issubclass(exc_type, KeyboardInterrupt):
            logger.error("Uncaught exception", exc_info=(exc_type, exc_value, exc_traceback))

    import sys
    sys.excepthook = handle_exception

    return logger


def log_and_ingest_failure(exception, test_case_name, error_type=None):
    """
    Logs the failure details and ingests them into Elasticsearch.
    :param exception: The exception object.
    :param test_case_name: Name of the test case.
    :param error_type: Optional; type of the error (default: detected from exception).
    """
    logger = get_logger(__name__)
    es_utility = ElasticSearchUtility(index_name="automation-logs")
    if not error_type:
        error_type = type(exception).__name__

    error_message = f"Test case {test_case_name} failed with error: {str(exception)}"
    logger.error(error_message, exc_info=True)  # Log error with traceback

    # Ingest error details into Elasticsearch
    '''es_utility.ingest_log({
        "test_case_name": test_case_name,
        "status": "FAIL",
        "error_type": error_type,
        "message": error_message
    })'''

def elk_logger(func):
    """Decorator to log the start, end, and exceptions for a test case."""
    @wraps(func)
    def wrapper(driver, request, *args, **kwargs):
        logger = get_logger(__name__)
        es_utility = ElasticSearchUtility(index_name="automation-logs")
        test_case_name = request.node.name
        logger.info(f"Starting test: {test_case_name}")
        allure.dynamic.title(test_case_name)

        try:
            result = func(driver, request, *args, **kwargs)  # Run the actual test
            logger.info(f"Test {test_case_name} passed successfully.")
            '''es_utility.ingest_log({
                "test_case_name": test_case_name,
                "status": "PASS",
                "message": f"Test {test_case_name} completed successfully."
            })'''
            return result

        except AssertionError as ae:
            allure.attach(logger.handlers[0].baseFilename, name="Assertion Failure Logs",
                          attachment_type=allure.attachment_type.TEXT)
            if driver:
                capture_screenshot(driver, test_case_name)
            log_and_ingest_failure(ae, test_case_name, "AssertionError")
            raise

        except Exception as e:
            allure.attach(logger.handlers[0].baseFilename, name="Error Logs",
                          attachment_type=allure.attachment_type.TEXT)
            if driver:
                capture_screenshot(driver, test_case_name)
            log_and_ingest_failure(e, test_case_name)
            raise

        finally:
            logger.info(f"Test {test_case_name} finished.")

    return wrapper


def capture_screenshot(driver, name="screenshot"):
    """Capture a screenshot and attach it to the Allure report."""
    screenshot_path = f"{name}.png"
    driver.save_screenshot(screenshot_path)
    allure.attach.file(screenshot_path, name="Screenshot", attachment_type=allure.attachment_type.PNG)


def attach_logs():
    """Attach log files to the Allure report."""
    with open("logs/app.log", "r") as log_file:
        allure.attach(log_file.read(), name="Test Logs", attachment_type=allure.attachment_type.TEXT)


def preserve_allure_history():
    """
    Copies the history folder from the last Allure report into the current allure-results directory
    to maintain history across test executions.
    """
    previous_report_dir = "allure-report"
    current_results_dir = "allure-results"

    # Check if the previous report exists
    history_src = os.path.join(previous_report_dir, "history")
    history_dest = os.path.join(current_results_dir, "history")

    if os.path.exists(history_src):
        print("Preserving Allure history...")
        shutil.copytree(history_src, history_dest, dirs_exist_ok=True)
    else:
        print("No previous Allure history found. Starting fresh.")
