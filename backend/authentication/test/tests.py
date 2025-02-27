import time
import pytest
from selenium import webdriver
from authentication.test.selenium_capabilities import enter_credentials, click_login, get_error_message
from selenium.webdriver.chrome.options import Options

BASE_URL = "http://localhost:3000"
VALID_CREDENTIALS = [("admin@gmail.com", "admin123"),
                     ("test_user@gmail.com", "test123")]
INVALID_CREDENTIALS = [
    ("admin@gmail.com", "wrongpassword"),  # Wrong password
    ("wronguser@example.com", "SecurePass1!"),  # Wrong email
    ("user@company", "SecurePass1!"),  # Missing domain extension
    ("test@random.xyz", "SecurePass1!"),  # Unrecognized domain
]

@pytest.fixture(scope="function")
def driver():
    """ Set up Selenium WebDriver in headless mode """
    options = Options()
    options.add_argument("--headless=new")

    driver = webdriver.Chrome(options=options)  # Fix: Pass options to Chrome
    driver.get(BASE_URL)
    yield driver
    driver.quit()


# TESTS
@pytest.mark.parametrize("email, password", INVALID_CREDENTIALS)
def test_invalid_login(driver, email, password):
    """ Test invalid logins with different credentials """
    enter_credentials(driver, email, password)
    click_login(driver)
    error_message = get_error_message(driver)
    assert "Invalid" in error_message, f"Test Failed: {email} was accepted!"
    print(f"\033[92mTest Passed: Invalid login blocked for {email}\033[0m")


@pytest.mark.parametrize("email, password",  [VALID_CREDENTIALS[0]])
def test_successful_login(driver, email, password):
    """ Test successful login with correct credentials """
    enter_credentials(driver, email, password)
    click_login(driver)
    time.sleep(2)
    assert driver.current_url == f"{BASE_URL}/dashboard", "Test Failed: Login did not redirect!"
    print("\033[92mTest Passed: Successfull Login\033[0m")


@pytest.mark.parametrize("email, password",[VALID_CREDENTIALS[1]])
def test_rate_limiting(driver, email, password):
    """ Tests login locking after too many attempts consequently"""
    email, _ = VALID_CREDENTIALS
    for _ in range(5):
        enter_credentials(driver, email, "wrongpassword")
        click_login(driver)

    enter_credentials(driver, email, "wrongpassword")
    click_login(driver)

    error_message = get_error_message(driver)
    assert "Too many failed attempts" in error_message, "Test Failed: Rate limiting!"
    print("\033[92mTest Passed: Rate Limiting\033[0m")


if __name__ == "__main__":
    pytest.main()
