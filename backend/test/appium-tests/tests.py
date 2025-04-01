from appium import webdriver
from appium.options.android import UiAutomator2Options
from credentials_test_cases import test_cases as credential_test_cases
from appium.webdriver.common.appiumby import AppiumBy
import time
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC

# Colors for terminal
GREEN = "\033[92m"
RED = "\033[91m"
RESET = "\033[0m"

# --- Appium setup ---
options = UiAutomator2Options()
options.platform_name = "Android"
options.device_name = "Medium Phone API 36"
options.app_package = "com.example.aisurveyapp"
options.app_activity = "com.example.aisurveyapp.MainActivity"
options.no_reset = True

try:
    driver = webdriver.Remote(
        command_executor="http://localhost:4723",
        options=options
    )
except Exception as e:
    print("❌ Appium failed to start session:")
    print(e)
    exit(1)


def restart_app():
    if driver.is_app_installed("com.example.aisurveyapp"):
        driver.terminate_app("com.example.aisurveyapp")
    else:
        print("App is not installed, skipping termination.")
    time.sleep(1)
    driver.activate_app("com.example.aisurveyapp")
    time.sleep(2)

    # Wait for login screen
    WebDriverWait(driver, 10).until(
        EC.presence_of_element_located((AppiumBy.ID, "com.example.aisurveyapp:id/email_input"))
    )


def attempt_login(email, password):
    email_field = driver.find_element(AppiumBy.ID, "com.example.aisurveyapp:id/email_input")
    password_field = driver.find_element(AppiumBy.ID, "com.example.aisurveyapp:id/password_input")
    login_button = driver.find_element(AppiumBy.ID, "com.example.aisurveyapp:id/login_button")

    email_field.clear()
    password_field.clear()

    email_field.send_keys(email)
    password_field.send_keys(password)

    time.sleep(0.5)
    login_button.click()
    time.sleep(2)

    return driver.current_activity


def run_login_test_cases(test_cases = credential_test_cases):
    restart_app()
    for i, case in enumerate(test_cases):
        print(f"\nTest {i}: {case['label']}")
        activity = attempt_login(case["email"], case["password"])

        success = "SurveyActivity" in activity
        if case["expect_success"]:
            if success:
                print(f"{GREEN}TEST SUCCEEDED{RESET}")
            else:
                print(f"{RED}TEST FAILED{RESET}")
        else:
            if success:
                print(f"{RED}TEST FAILED{RESET}")
            else:
                print(f"{GREEN}TEST SUCCEDED{RESET}")


run_login_test_cases(credential_test_cases)

driver.quit()