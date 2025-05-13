import time
from selenium.webdriver.common.by import By

# SELENIUM CAPABILITIES
def enter_credentials(driver, email, password):
    """Selenium enters login credentials """
    email_input = driver.find_element(By.NAME, "email")
    password_input = driver.find_element(By.NAME, "password")
    email_input.clear()
    password_input.clear()
    email_input.send_keys(email)
    password_input.send_keys(password)


def click_login(driver):
    """ Helper function to click login button """
    login_button = driver.find_element(By.XPATH, "//button[text()='Login']")
    login_button.click()
    time.sleep(2)

def click_google_login(driver):
    """ Helper function to click google login button """
    google_login_button = driver.find_element(By.NAME, "google-login")
    google_login_button.click()
    time.sleep(2)

def get_error_message(driver):
    """ Helper function to get error message """
    try:
        return driver.find_element(By.CLASS_NAME, "error-message").text
    except:
        return ""
