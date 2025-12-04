from selenium.webdriver.common.by import By
from selenium.webdriver.support import expected_conditions as EC
from selenium.common.exceptions import WebDriverException, TimeoutException
from selenium.webdriver.support.ui import WebDriverWait
import pytest
import time

# ---------------------------
# Hover tests
# ---------------------------
@pytest.mark.parametrize("index", [0, 1, 2, 3, 4])
def test_check_hover_to_follow(driver, index):
    driver.get("https://www.cnarios.com/concepts/button#try-it-yourself")
    wait = WebDriverWait(driver, 10)
    
    try:
        spans = wait.until(EC.presence_of_all_elements_located((By.CSS_SELECTOR, "span[aria-label]")))
    except TimeoutException:
        pytest.skip("No span elements found")
    
    if index >= len(spans):
        pytest.skip(f"No span at index {index}")

    aria_label = spans[index].get_attribute("aria-label")
    print(f"Span {index} aria-label:", aria_label)
    assert aria_label == "Click to follow"


@pytest.mark.parametrize("index", [0, 1, 2, 3, 4])
def test_check_hover_to_unfollow(driver, index):
    driver.get("https://www.cnarios.com/concepts/button#try-it-yourself")
    wait = WebDriverWait(driver, 10)
    
    try:
        spans = wait.until(EC.presence_of_all_elements_located((By.CSS_SELECTOR, "span[aria-label]")))
    except TimeoutException:
        pytest.skip("No span elements found")
    
    if index >= len(spans):
        pytest.skip(f"No span at index {index}")

    aria_label = spans[index].get_attribute("aria-label")
    print(f"Span {index} aria-label:", aria_label)
    assert aria_label == "Click to unfollow"


# ---------------------------
# Follow/Unfollow button clicks
# ---------------------------
@pytest.mark.parametrize("index", [0, 1, 2, 3, 4])
def test_button_click(driver, index):
    driver.get("https://www.cnarios.com/concepts/button#try-it-yourself")
    wait = WebDriverWait(driver, 10)
    
    try:
        btns = wait.until(EC.presence_of_all_elements_located((By.CSS_SELECTOR, "button.css-nqtpxt")))
    except TimeoutException:
        pytest.skip("No follow buttons found")
    
    if index >= len(btns):
        pytest.skip(f"No button at index {index}")

    try:
        wait.until(EC.element_to_be_clickable(btns[index]))
        btns[index].click()
    except WebDriverException as e:
        pytest.fail(f"Button {index} click failed: {e}")


@pytest.mark.parametrize("index", [0, 1, 2, 3, 4])
def test_check_following(driver, index):
    driver.get("https://www.cnarios.com/concepts/button#try-it-yourself")
    wait = WebDriverWait(driver, 10)
    
    try:
        btns = wait.until(EC.presence_of_all_elements_located((By.CSS_SELECTOR, "button.css-18jle08")))
    except TimeoutException:
        pytest.skip("No following buttons found")
    
    if index >= len(btns):
        pytest.skip(f"No button at index {index}")

    button_text = btns[index].text.strip()
    print(f"Button {index} text:", button_text)
    assert button_text == "Following"


@pytest.mark.parametrize("index", [0, 1, 2, 3, 4])
def test_unfollow_click_button(driver, index):
    driver.get("https://www.cnarios.com/concepts/button#try-it-yourself")
    wait = WebDriverWait(driver, 10)
    
    try:
        btns = wait.until(EC.presence_of_all_elements_located((By.CSS_SELECTOR, "button.css-18jle08")))
    except TimeoutException:
        pytest.skip("No following buttons found")
    
    if index >= len(btns):
        pytest.skip(f"No button at index {index}")

    try:
        wait.until(EC.element_to_be_clickable(btns[index]))
        btns[index].click()
    except WebDriverException as e:
        pytest.fail(f"Button {index} click failed: {e}")


@pytest.mark.parametrize("index", [0, 1, 2, 3, 4])
def test_follow_button_click_after_shows_processing_text(driver, index):
    driver.get("https://www.cnarios.com/concepts/button#try-it-yourself")
    wait = WebDriverWait(driver, 10)

    try:
        btns = wait.until(EC.presence_of_all_elements_located((By.CSS_SELECTOR, "button.css-nqtpxt")))
    except TimeoutException:
        pytest.skip("No follow buttons found")
    
    if index >= len(btns):
        pytest.skip(f"No button at index {index}")

    button = btns[index]

    try:
        wait.until(EC.element_to_be_clickable(button))
        button.click()
    except WebDriverException:
        pytest.fail(f"Button {index} click failed")

    try:
        btns_messages = wait.until(EC.presence_of_all_elements_located((By.CSS_SELECTOR, "button.css-18jle08")))
        if index >= len(btns_messages):
            pytest.skip(f"No following button at index {index}")
        
        button_text = btns_messages[index].text.strip()
        print(f"Button {index} text after click:", button_text)
        assert button_text == "Processing..."
    except Exception as e:
        pytest.fail(f"Button {index} did not show 'Processing...' text: {e}")


# ---------------------------
# Remove suggestion cards
# ---------------------------
def test_remove_all_suggestion_cards(driver):
    driver.get("https://www.cnarios.com/concepts/button#try-it-yourself")
    wait = WebDriverWait(driver, 10)

    while True:
        try:
            btns = wait.until(EC.presence_of_all_elements_located((By.CSS_SELECTOR, "button.css-xz9haa")))
        except TimeoutException:
            print("No more remove buttons found.")
            break 

        button = btns[0]
        try:
            wait.until(EC.element_to_be_clickable(button))
            button.click()
            print("Clicked a remove button.")
            time.sleep(0.5)  # small delay for DOM update
        except WebDriverException:
            pytest.fail("Failed to click remove button")
