from selenium.webdriver.common.by import By
from selenium.webdriver.remote.webelement import WebElement
from selenium.webdriver.support.ui import WebDriverWait
from typing import Tuple, List
from typing import Optional
import time
from selenium.webdriver.support import expected_conditions as EC
Credentials = Tuple[str, str]

admin = ("admin", "admin123")
user = ("user", "user123")
admin_wrong_password = ("admin", "admin2323")
user_wrong_password = ("user", "user132323")
empty_fields = ("","")

def login_credentials(credentials: Credentials, inputs: List[WebElement]) -> None:
    inputs[0].send_keys(credentials[0])
    inputs[1].send_keys(credentials[1])

def submit_button(driver) -> None:
    try:
        button = driver.find_element(
            By.CSS_SELECTOR,
            "button.MuiButton-root.MuiButton-containedPrimary"
        )
        button.click()
    except Exception as e:
        print("Login button not found:", e)

def clear_inputs(inputs: List[WebElement]) -> None:
    for input_field in inputs:
        input_field.clear()

def check_login_admin(driver, inputs: List[WebElement]) -> None:
    login_credentials(admin, inputs)
    submit_button(driver)
    alert_message = text_on_page_after_login(driver) 
    assert alert_message == "ADMIN", f"Test failed because alert_message was '{alert_message}'"
        

def check_login_user(driver, inputs: List[WebElement]) -> None:
    login_credentials(user, inputs)
    submit_button(driver)
    alert_message = text_on_page_after_login(driver) 
    assert alert_message == "USER", f"Test failed because alert_message was '{alert_message}'"

def click_logout(driver) -> None:
    try:
        button = driver.find_element(
            By.CSS_SELECTOR,
            "button.MuiButton-outlinedSecondary"
        )
        button.click()
    except Exception as e:
        print("Logout button not found:", e)
    time.sleep(5)
    
def text_on_page_after_login(driver) -> Optional[str]:
    try:
            status_element = driver.find_element(
                By.CSS_SELECTOR, 
                "strong"  
            )
            return status_element.text
    except Exception as e:
        print("Status element not found:", e)
        return None

def page_load_inputs(driver):
    inputs = driver.find_elements(
        By.CSS_SELECTOR,
        ".MuiInputBase-input.MuiOutlinedInput-input.MuiInputBase-inputSizeSmall.css-15v65ck"
    )
    return inputs


def test_positive_admin(driver):
    driver.get("https://www.cnarios.com/challenges/login-flow")
    inputs = page_load_inputs(driver)
    check_login_admin(driver, inputs)
    click_logout(driver)

def test_positive_user(driver):
    driver.get("https://www.cnarios.com/challenges/login-flow")
    inputs = page_load_inputs(driver)
    check_login_user(driver, inputs)
    click_logout(driver)

def check_alert_incorrect_password(driver):
    try:
        status_element = driver.find_element(
            By.XPATH,
            "//*[contains(@class, 'MuiAlert-message') and contains(text(), 'Invalid username or password')]"
        )
        return status_element.text
    except Exception as e:
        print("Status element not found:", e)
        return None

def check_login_admin_incorrect_password(driver, inputs):
    login_credentials(admin_wrong_password, inputs)
    submit_button(driver)
    alert_message = check_alert_incorrect_password(driver)
    assert alert_message == "Invalid username or password.", f"Test failed because alert_message was '{alert_message}'"

def test_negative_admin(driver):
    driver.get("https://www.cnarios.com/challenges/login-flow")
    inputs = page_load_inputs(driver)
    check_login_admin_incorrect_password(driver, inputs)

def check_login_user_incorrect_password(driver, inputs):
    login_credentials(user_wrong_password, inputs)
    submit_button(driver)
    alert_message = check_alert_incorrect_password(driver)
    assert alert_message == "Invalid username or password.", f"Test failed because alert_message was '{alert_message}'"

def test_negative_user(driver):
    driver.get("https://www.cnarios.com/challenges/login-flow")
    inputs = page_load_inputs(driver)
    check_login_user_incorrect_password(driver, inputs)

def get_alert_message_after_login_attempt_empty_fields(driver):
    try:
        status_element = driver.find_element(
            By.XPATH,
            "//*[contains(@class, 'MuiAlert-message') and contains(text(), 'Both fields are required')]"
        )
        return status_element.text
    except Exception as e:
        print("Status element not found:", e)
        return None

def check_empty_fields_validation(driver, inputs: List[WebElement]) -> None:
    login_credentials(empty_fields, inputs)
    submit_button(driver)
    alert_message = get_alert_message_after_login_attempt_empty_fields(driver)

    assert alert_message == "Both fields are required.", f"Test failed because alert_message was '{alert_message}'"


def get_login_page(driver):
    try:
        status_element = driver.find_element(
            By.XPATH,
            "//*[contains(@class, 'MuiTypography-h5') and contains(text(), 'Login')]"
        )
        return status_element.text
    except Exception as e:
        print("Status element not found:", e)
        return None

def assert_logout_resets_session(driver) -> None:
    login_page = get_login_page(driver)
    assert login_page == "Login", f"Test failed because login_page was '{login_page}'"

def test_empty_fields_validation(driver):
    driver.get("https://www.cnarios.com/challenges/login-flow")
    inputs = page_load_inputs(driver)
    check_empty_fields_validation(driver, inputs)

def test_logout_resets_session(driver):
    driver.get("https://www.cnarios.com/challenges/login-flow")
    inputs = page_load_inputs(driver)
    check_login_user(driver, inputs)
    click_logout(driver)
    assert_logout_resets_session(driver)


