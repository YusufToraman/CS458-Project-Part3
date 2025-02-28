import json
import time
import pytest
from selenium import webdriver
from authentication.test.selenium_capabilities import enter_credentials, click_login, get_error_message, click_google_login
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys

BASE_URL = "http://localhost:3000"
VALID_CREDENTIALS = [("admin@gmail.com", "admin123"),
                     ("test_user@gmail.com", "test123")]
INVALID_CREDENTIALS = [
    ("", ""), # Empty fields
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
    
def setup_driver():
    """ Set up Selenium WebDriver in headless mode """
    options = Options()
    # options.add_argument("--headless=new")

    driver = webdriver.Chrome(options=options)  # Fix: Pass options to Chrome
    driver.get(BASE_URL)
    return driver


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


@pytest.mark.parametrize("email, password", [VALID_CREDENTIALS[0]])
def test_login_state_persistancy(driver, email, password):
    """ Test if login state persists after refresh """
    enter_credentials(driver, email, password)
    click_login(driver)
    time.sleep(2)
    user = json.loads(driver.get_cookie("user")["value"])
    time.sleep(2)
    assert user == email, "Test Failed: Login state not persisted!"
    driver.refresh()
    driver.get(BASE_URL)
    time.sleep(2)
    assert driver.current_url == f"{BASE_URL}/dashboard", "Test Failed: Login state not persisted"


    print("\033[92mTest Passed: Login State Persisted\033[0m")

@pytest.mark.parametrize("email, password", [VALID_CREDENTIALS[0]])
def test_google_login(driver:webdriver.Chrome, email, password):
    """ Test Google login """
    import dotenv
    import os
    dotenv.load_dotenv()
    gmailId = os.getenv('G_MAIL')
    passWord = os.getenv('G_PASS')
    driver=setup_driver()

    driver.get(r'https://accounts.google.com/signin/v2/identifier?continue='+\
    'https%3A%2F%2Fmail.google.com%2Fmail%2F&amp;service=mail&amp;sacu=1&amp;rip=1'+\
    '&amp;flowName=GlifWebSignIn&amp;flowEntry = ServiceLogin')
    driver.implicitly_wait(15)
    loginBox = driver.find_element(By.XPATH,'//*[@id="identifierId"]')
    loginBox.send_keys(gmailId)
    loginBox.send_keys(Keys.ENTER)
    time.sleep(2)
    passWordBox = driver.find_element(By.CSS_SELECTOR, 'input[type="password"]')
    passWordBox.send_keys(passWord)
    passWordBox.send_keys(Keys.ENTER)
    time.sleep(5)
    driver.get(BASE_URL)
    click_google_login(driver)
    time.sleep(2)

    # go to popup window
    driver.switch_to.window(driver.window_handles[1])
    print(driver.window_handles)
    time.sleep(2)
    # get data-identifier="burakdemirel49@gmail.com" field
    user = driver.find_element(By.CSS_SELECTOR, 'div[data-identifier="'+ gmailId + '"]')
    user.click()
    # select whole page
    time.sleep(2)
    html = driver.find_element(By.XPATH, '//span[text()="Devam Et"]').click()
    time.sleep(2)
    driver.switch_to.window(driver.window_handles[0])
    time.sleep(2)
    user = json.loads(driver.get_cookie("user")["value"])
    time.sleep(2)
    assert user == gmailId, "Test Failed: Login state not persisted!"
    print("\033[92mTest Passed: Google Login\033[0m")


@pytest.mark.parametrize("email, password", [VALID_CREDENTIALS[0]])
def test_ui_user_friendliness(driver, email, password):
    """ Test if UI is user friendly """
    email_input = driver.find_element(By.NAME, "email")
    email_input.clear()
    email_input.send_keys(email)
    email_input.send_keys(Keys.TAB)
    time.sleep(2)
    # fill the password field
    driver.switch_to.active_element.send_keys(password)
    driver.switch_to.active_element.send_keys(Keys.ENTER)
    time.sleep(2)
    assert driver.current_url == f"{BASE_URL}/dashboard", "Test Failed: User friendly UI"
    print("\033[92mTest Passed: User Friendly UI\033[0m")



if __name__ == "__main__":
    pytest.main()


