from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.common.by import By
import time

def setup_driver():
    options = Options()
    options.add_argument("--log-level=3")
    options.add_experimental_option("excludeSwitches", ["enable-logging"])
    return webdriver.Chrome(options=options)

def get_rgb(value):
    return tuple(map(int, value.strip("rgba()").split(",")[:3]))

def print_passed(message):
    print(f"[PASSED] - {message}")

def print_failed(message):
    print(f"[FAILED] - {message}")

def run_tests():
    print("Beginning Tests - Daniel Werner\n")
    driver = setup_driver()
    try:
        driver.get("http://localhost:5000/loginscreen")
        time.sleep(1)

        # --- Button Existence and Color ---
        login_button = driver.find_element(By.CSS_SELECTOR, "input[type='submit'][value='Login']")
        print_passed("Login Button Exists")

        login_color = get_rgb(login_button.value_of_css_property("background-color"))
        if login_color == (47, 95, 118):
            print_passed("Login Button is #2F5F76")
        else:
            print_failed(f"Login Button color mismatch: {login_color}")

        signup_button = driver.find_element(By.CSS_SELECTOR, "input[type='submit'][value='Create Account']")
        print_passed("Create User Button Exists")

        signup_color = get_rgb(signup_button.value_of_css_property("background-color"))
        if signup_color == (47, 95, 118):
            print_passed("Create User Button is #2F5F76")
        else:
            print_failed(f"Create User Button color mismatch: {signup_color}")

        # --- Slider Toggle ---
        login_btn = driver.find_element(By.ID, "loginButton")
        signup_btn = driver.find_element(By.ID, "signinButton")
        login_form = driver.find_element(By.ID, "ImLoggingIn")
        signup_form = driver.find_element(By.ID, "ImCreatingAnAccount")

        if login_form.is_displayed() and not signup_form.is_displayed():
            print_passed("Initial state: Login visible, Signup hidden")
        signup_btn.click()
        time.sleep(0.5)
        if signup_form.is_displayed() and not login_form.is_displayed():
            print_passed("Signup form visible, Login hidden after toggle")
        login_btn.click()
        time.sleep(0.5)
        if login_form.is_displayed() and not signup_form.is_displayed():
            print_passed("Login form visible, Signup hidden after re-toggle")

        # --- Password Toggle for Login Form ---
        pwd_input = driver.find_element(By.ID, "password_input")
        eye_icon = driver.find_element(By.XPATH, "//div[@id='ImLoggingIn']//img[contains(@class,'passwordToggleIcon')]")

        eye_icon.click()
        time.sleep(0.3)
        if pwd_input.get_attribute("type") == "text":
            print_passed("Password shows on toggle (Login form)")
        eye_icon.click()
        time.sleep(0.3)
        if pwd_input.get_attribute("type") == "password":
            print_passed("Password hides on second toggle (Login form)")

        # --- Password Toggle for Signup Form ---
        signup_btn.click()
        time.sleep(0.5)

        new_pwd = driver.find_element(By.ID, "new_password")
        new_eye = driver.find_element(By.XPATH, "//div[@id='ImCreatingAnAccount']//img[contains(@class,'passwordToggleIcon')]")

        new_eye.click()
        time.sleep(0.3)
        if new_pwd.get_attribute("type") == "text":
            print_passed("Password shows on toggle (Signup form)")
        new_eye.click()
        time.sleep(0.3)
        if new_pwd.get_attribute("type") == "password":
            print_passed("Password hides on second toggle (Signup form)")

        # --- Add image toggle test here if applicable ---

    except Exception as e:
        print("[ERROR]", e)

    finally:
        print("\nEnding Tests")
        driver.quit()

if __name__ == "__main__":
    run_tests()
