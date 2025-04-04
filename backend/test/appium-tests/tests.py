from appium import webdriver
from appium.options.android import UiAutomator2Options
from credentials_test_cases import test_cases as credential_test_cases, valid_credential, email_sent_test_cases
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
    package_name = "com.example.aisurveyapp"

    if driver.is_app_installed(package_name):
        try:
            # This forces the app to stop immediately
            driver.terminate_app(package_name, options={"forceStop": True})
        except Exception as e:
            print(f"{RED}Warning: terminate_app failed, skipping termination. Error: {e}{RESET}")
    else:
        print("App is not installed, skipping termination.")

    time.sleep(1)
    driver.activate_app(package_name)
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


def test_email_sent_confirmation(email: str):
    driver.find_element(AppiumBy.ID, "com.example.aisurveyapp:id/email_input").send_keys(email)
    time.sleep(0.5)
    driver.find_element(AppiumBy.ID, "com.example.aisurveyapp:id/name_input").send_keys("John Doe")
    time.sleep(0.5)
    driver.find_element(AppiumBy.ID, "com.example.aisurveyapp:id/birthdate_input").send_keys("01/01/2000")
    time.sleep(0.5)
    driver.find_element(AppiumBy.ID, "com.example.aisurveyapp:id/city_input").send_keys("Istanbul")
    time.sleep(0.5)
    driver.find_element(AppiumBy.ID, "com.example.aisurveyapp:id/usecase_input").send_keys("Writing code")
    time.sleep(0.5)
    driver.find_element(AppiumBy.ID, "com.example.aisurveyapp:id/gender_male").click()
    time.sleep(0.5)
    driver.find_element(AppiumBy.ID, "com.example.aisurveyapp:id/chatgpt_check").click()
    time.sleep(0.5)
    cons_field = driver.find_element(AppiumBy.XPATH, '//android.widget.EditText[contains(@hint, "ChatGPT - Cons")]')
    time.sleep(0.5)
    cons_field.send_keys("Sometimes inaccurate")
    time.sleep(0.5)
    driver.find_element(AppiumBy.ID, "com.example.aisurveyapp:id/send_button").click()

    try:
        toast = WebDriverWait(driver, 5).until(
            EC.presence_of_element_located(
                (AppiumBy.XPATH, "//android.widget.Toast[@text='Survey is submitted! Email sent.']")
            )
        )
        return True
    except:
        # Maybe it's a failure toast
        try:
            toast = driver.find_element(
                AppiumBy.XPATH,
                "//android.widget.Toast[@text='Submission failed.']"
            )
            return False
        except:
            return False

def clear_fields():
    # Clear EditText fields
    driver.find_element(AppiumBy.ID, "com.example.aisurveyapp:id/email_input").clear()
    driver.find_element(AppiumBy.ID, "com.example.aisurveyapp:id/name_input").clear()
    driver.find_element(AppiumBy.ID, "com.example.aisurveyapp:id/birthdate_input").clear()
    driver.find_element(AppiumBy.ID, "com.example.aisurveyapp:id/city_input").clear()
    driver.find_element(AppiumBy.ID, "com.example.aisurveyapp:id/usecase_input").clear()

    # Clear radio selection by clicking the selected one again (toggle off doesn't exist in native Android)
    try:
        selected_radio = driver.find_element(AppiumBy.XPATH, "//android.widget.RadioButton[@checked='true']")
        selected_radio.click()  # will toggle if your implementation allows
    except:
        pass  # nothing was selected

    # Uncheck all checkboxes (AI models)
    for checkbox_id in [
        "com.example.aisurveyapp:id/chatgpt_check",
        "com.example.aisurveyapp:id/bard_check",
        "com.example.aisurveyapp:id/claude_check",
        "com.example.aisurveyapp:id/copilot_check"
    ]:
        checkbox = driver.find_element(AppiumBy.ID, checkbox_id)
        is_checked = checkbox.get_attribute("checked") == "true"
        if is_checked:
            checkbox.click()

    # Clear dynamically generated cons fields (if any)
    try:
        cons_container = driver.find_element(AppiumBy.ID, "com.example.aisurveyapp:id/cons_container")
        cons_inputs = cons_container.find_elements(AppiumBy.CLASS_NAME, "android.widget.EditText")
        for field in cons_inputs:
            field.clear()
    except:
        pass  # container might be empty


def run_sent_email_test(test_cases = email_sent_test_cases):
    print("\n\n--- Email Sent Confirmation Tests ---")
    restart_app()
    attempt_login(valid_credential["email"], valid_credential["password"])
    for i, case in enumerate(test_cases):
        print(f"\nTest {i}: {case['label']}")
        clear_fields()
        res = test_email_sent_confirmation(case["email"])
        if case["expect_success"]:
            if res:
                print(f"{GREEN}TEST SUCCEEDED{RESET}")
            else:
                print(f"{RED}TEST FAILED{RESET}")
        else:
            if res:
                print(f"{RED}TEST FAILED{RESET}")
            else:
                print(f"{GREEN}TEST SUCCEEDED{RESET}")


run_login_test_cases(credential_test_cases)
run_sent_email_test()
driver.quit()


