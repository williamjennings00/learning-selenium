# conftest.py
import pytest
from selenium import webdriver
from selenium.webdriver.chrome.service import Service as ChromeService
from webdriver_manager.chrome import ChromeDriverManager
from selenium.webdriver.support.ui import WebDriverWait

TEST_PAGE_URL = 'https://www.cnarios.com/concepts/button#try-it-yourself'

@pytest.fixture(scope="session")
def page_url():
    """Provides the URL for the test page."""
    return TEST_PAGE_URL

@pytest.fixture(scope="session")
def driver():
    print("\n--- Starting Chrome WebDriver ---")
    
    options = webdriver.ChromeOptions()
    # options.add_argument("--headless=new")  # safer for macOS
    
    _driver = webdriver.Chrome(options=options)  
    _driver.maximize_window()
    _driver.implicitly_wait(5)

    yield _driver
    print("--- Quitting Chrome WebDriver ---")
    _driver.quit()


@pytest.fixture(scope="function")
def wait(driver):
    """Provides a WebDriverWait instance for explicit waits."""
    return WebDriverWait(driver, 10) # 10-second timeout for explicit waits
