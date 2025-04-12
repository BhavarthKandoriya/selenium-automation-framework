# 🧪 Selenium Automation Framework (Python)

A robust, scalable, and maintainable Selenium automation framework built using Python, Pytest, and Allure, with integrations for distributed test execution and advanced logging via ELK Stack.

---

## 🚀 Key Features

- ✅ **Page Object Model (POM)** design pattern for maintainability and reusability.
- ✅ **Environment-specific test data** managed using `.env` files.
- ✅ **Separate locator files per page** under `/locators`.
- ✅ **Selenium Grid** support for distributed execution.
- ✅ **Parallel test execution** using `pytest-xdist`.
- ✅ **Allure Reporting** with screenshots, logs, and historical test results.
- ✅ **Centralized logging** using ELK Stack (Elasticsearch, Logstash, Kibana).
- ✅ **Custom decorators** for logging, screenshot capture, and exception handling.
- ✅ **Common Utilities:** Provides reusable utility modules for:
    * `selenium_actions.py`: Wrapper functions for common Selenium interactions (clicks, send keys, waits) with built-in logging and error handling.
    * `elasticsearch_utils.py`: Functions to connect and send data to Elasticsearch.
    * `common_utils.py`: General helper functions, screenshot utilities, decorator implementations.
    * `webdriver_factory.py`: Handles WebDriver instance creation for different browsers (local and remote/Grid).

---

## 📁 Project Structure
    ├── .docker                   # Folder with docker-compose file to spin up the selenium hub and nodes
    ├── locators                  # Folder which contains separate locator files per page
    ├── pages                     # Folder containing separe page classes to interact with the locators
    ├── tests                     # Folder containing test scripts
    ├── utilities                 # Scripts for reusable utilities for Selenium actions, logging etc
    ├── .env.staging              # Staging environment file
    ├── .env.dev                  # Development environment file
    ├── conftest.py
    ├── README.md                 # Readme file
    └── app.log                   # File with execution logs 


## Prerequisites

* Python 3.8+
* pip (Python package installer)
* Git
* Web Browsers (e.g., Chrome, Firefox)
* Corresponding WebDriver binaries (e.g., chromedriver, geckodriver). Consider using `webdriver-manager` (if included in `requirements.txt`) for automatic management, or ensure they are in your system's PATH.
* Allure Commandline: Required for generating the HTML report. Installation instructions: [https://docs.qameta.io/allure/#_installing_a_commandline](https://docs.qameta.io/allure/#_installing_a_commandline)
* (Optional) Docker and Docker Compose: If you plan to run tests against a Selenium Grid instance managed via Docker.
* (Optional) Access to an Elastic Stack instance (Elasticsearch, Kibana) if you intend to use the monitoring features.

## Installation & Setup

1.  **Clone the repository:**
    ```bash
    git clone <your-repository-url>
    cd selenium-automation-framework
    ```

2.  **Create and activate a virtual environment (Recommended):**
    ```bash
    python -m venv venv
    # On Windows
    venv\Scripts\activate
    # On macOS/Linux
    source venv/bin/activate
    ```

3.  **Install dependencies:**
    ```bash
    pip install -r requirements.txt
    ```

4.  **Configure Environment Variables:**
    * Create environment-specific `.env` files (e.g., `.env.qa`, `.env.dev`) in the project root directory based on the templates or requirements.
    * Populate these files with necessary configurations. Example `.env.qa`:
        ```dotenv
        # Application Details
        BASE_URL=[https://qa.yourapplication.com](https://qa.yourapplication.com)
        ADMIN_USERNAME=qa_user
        ADMIN_PASSWORD=your_secure_password

        # Selenium Grid Configuration (Leave empty or comment out for local execution)
        SELENIUM_GRID_URL=http://localhost:4444/wd/hub
        # BROWSER=chrome # Specify default browser if needed

        # Elasticsearch Configuration (Optional)
        ELASTICSEARCH_HOST=http://localhost:9200
        ELASTICSEARCH_INDEX=automation-logs
        # ELASTICSEARCH_USER=elastic # If authentication is enabled
        # ELASTICSEARCH_PASSWORD=changeme # If authentication is enabled
        ```
    * **Important:** Ensure your actual `.env.*` files are added to `.gitignore` to prevent committing sensitive data.

5.  **Install Allure Commandline:** Follow the official instructions linked in the Prerequisites section. Verify installation with `allure --version`.

6.  **Setup Selenium Grid (Optional):** If using remote execution, ensure your Selenium Grid is running and accessible at the URL specified in `SELENIUM_GRID_URL`.

## Running Tests

Tests are executed using `pytest`. The framework uses a custom command-line option `--env` to specify which environment configuration (`.env.{env}`) to load.

1.  **Clear Previous Allure Results (Optional but Recommended):**
    ```bash
    # On macOS/Linux
    rm -rf allure-results/*
    # On Windows (Command Prompt)
    if exist allure-results rmdir /s /q allure-results && mkdir allure-results
    # On Windows (PowerShell)
    if (Test-Path allure-results) { Remove-Item -Recurse -Force allure-results } ; New-Item -ItemType Directory -Name allure-results
    ```

2.  **Run Tests for a Specific Environment (e.g., QA):**
    ```bash
    pytest tests/ --env qa --alluredir=allure-results
    ```
    * `tests/`: Specifies the directory containing the tests.
    * `--env qa`: Loads configuration from `.env.qa`. Replace `qa` with `dev`, `prod`, etc., as needed.
    * `--alluredir=allure-results`: Specifies the directory to store raw Allure result files.

3.  **Run Tests in Parallel (using pytest-xdist):**
    Specify the number of parallel workers (`-n`). `auto` attempts to use the number of available CPU cores.
    ```bash
    pytest tests/ --env qa -n auto --alluredir=allure-results
    # Or specify a fixed number of workers
    pytest tests/ --env qa -n 4 --alluredir=allure-results
    ```

4.  **Run Specific Test Files or Test Cases:**
    ```bash
    # Run a specific file
    pytest tests/test_user_login.py --env qa --alluredir=allure-results

    # Run tests matching a keyword expression (-k)
    pytest tests/ --env qa -k "login and valid" --alluredir=allure-results

    # Run tests with a specific marker (-m) (if markers are defined, e.g., @pytest.mark.smoke)
    pytest tests/ --env qa -m smoke --alluredir=allure-results
    ```

## Reporting with Allure

After running tests with the `--alluredir` option, you can generate and view the HTML report.

1.  **Generate the Report:**
    This command processes the files in `allure-results` and creates the report in `allure-report`. The `--clean` flag removes previous report data.
    ```bash
    allure generate allure-results --clean -o allure-report
    ```

2.  **Open the Report:**
    This command starts a local web server and opens the generated report in your default browser.
    ```bash
    allure open allure-report
    ```

The Allure report provides interactive visualizations of test results, including:
* Overview dashboard with pass/fail statistics.
* Categorized test results (by suite, feature, severity).
* Detailed steps for each test.
* Execution timeline.
* Historical trend data.
* Attached screenshots.
* Attached logs.

## Adding New Locators

To add a locator for a new element on a page:

1.  **Identify the Page:** Determine which page the element belongs to (e.g., `HomePage`).
2.  **Open Locator File:** Navigate to the corresponding file in the `locators/` directory (e.g., `locators/home_page_elements.py`). If the file doesn't exist, create it.
3.  **Define Locator Variable:** Add a new key inside elements dictionary representing the element. The value should be a tuple containing the Selenium `By` strategy and the locator string.
    ```python
    # Example within locators/home_page_elements.py
    from selenium.webdriver.common.by import By

    elements = {
    '_log_in_link': (By.ID, 'login2'),
    '_log_in_button': (By.XPATH, '//button[text()="Log in"]'),
    '_username_input': (By.ID, 'loginusername'),
    '_password_input': (By.ID, 'loginpassword')
    }
    ```
4.  **Use in Page Object:**
    * Import the locator class into the corresponding Page Object file (e.g., `pages/home_page.py`).
    * Use the imported locator variable within the page methods when interacting with the element, typically passing it to your custom Selenium action wrappers.
    ```python
    # Example within pages/home_page.py
    from locators import HomePageLocators
    from utilities.selenium_actions import SeleniumActions # Assuming SeleniumActions class handles driver/actions

    class LoginPage(SeleniumActions):
    def __init__(self, driver):
        super().__init__(driver)
        self.home_elements = home_page_elements.elements
        self.logger = get_logger(__name__)

    def enter_username_password(self, username, password):
        self.find_and_type(*self.home_elements.get('_username_input'), username)
        self.find_and_type(*self.home_elements.get('_password_input'), password)
        self.find_and_click(*self.home_elements.get('_log_in_button'))
        return ProductsPage(self.driver)

    def validate_error_message(self):
        return self.get_alert_text()
    ```

## Logging and Monitoring

* **File Logging:** All test execution logs are appended to `app.log` in the project root directory. 
* **Elastic Stack:** If configured in the `.env` file, logs and potentially test result summaries are sent to the specified Elasticsearch instance. This allows for creating Kibana dashboards to visualize test trends, failure rates, execution times, and perform detailed log analysis across multiple runs. The `utilities/elasticsearch_utils.py` module handles the connection and data ingestion logic. 

---
