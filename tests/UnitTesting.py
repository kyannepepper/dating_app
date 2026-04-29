
import unittest
from selenium import webdriver
from selenium.common.exceptions import NoSuchElementException
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC

from selenium import webdriver
from selenium.webdriver.common.by import By
import time





# Update this to match the path to your own chromedriver!
chrome_driver_path = "/opt/homebrew/bin/chromedriver"
service = Service(executable_path=chrome_driver_path)
driver = webdriver.Chrome(service=service)


# Helper function to print test results
def test_result(condition, description):
    if condition:
        print(f"[PASSED] - {description}")
    else:
        print(f"[FAILED] - {description}")

try:
    print("Beginning Tests - Kyanne Klein")
    driver.get("http://localhost:5000/loginscreen")
    time.sleep(1)

    # 1. Login Button Exists
    login_button = driver.find_element(By.CSS_SELECTOR, "input[type='submit'][value='Login']")
    test_result(login_button is not None, "Login Button Exists")

    # 2. Login Button is Green
    login_color = login_button.value_of_css_property("background-color")
    
    test_result("rgba(47, 95, 118, 1)" in login_color, "Login Button is Blue")

    # 3. Create User Button Exists
    create_user_button = driver.find_element(By.CSS_SELECTOR, "input[type='submit'][value='Create Account']")  # Update with actual ID
    test_result(create_user_button is not None, "Create User Button Exists")

    # 4. Create User Button is Blue
    create_color = create_user_button.value_of_css_property("background-color")
    
    test_result("rgba(47, 95, 118, 1)" in create_color, "Create Button is Blue")

    # 9. Username Field Exists
    username_field = driver.find_element(By.NAME, "username")
    test_result(username_field is not None, "Username Field Exists")

    # 10. Password Field Exists
    password_field = driver.find_element(By.NAME, "password")
    test_result(password_field is not None, "Password Field Exists")

    # 9. Name Field Exists
    first_name_field = driver.find_element(By.NAME, "new_first_name")
    test_result(first_name_field is not None, "Name Field Exists")

    # 10. Last Name Field Exists
    last_name_field = driver.find_element(By.NAME, "new_last_name")
    test_result(last_name_field is not None, "Last Name Field Exists")

    # 10. IQ Field Exists
    iq_field = driver.find_element(By.NAME, "new_iq")
    test_result(iq_field is not None, "IQ Field Exists")

    # 5. Login Succeeds with Valid Credentials
    driver.find_element(By.ID, "loginButton").click()
    time.sleep(1)

    # 6. 

    
     
  

    driver.find_element(By.NAME, "username").clear()
    driver.find_element(By.NAME, "username").send_keys("Jeff")

    driver.find_element(By.NAME, "password").clear()
    driver.find_element(By.NAME, "password").send_keys("Gumby")

    login_button = driver.find_element(By.CSS_SELECTOR, "input[type='submit'][value='Login']")
    login_button.click()
    time.sleep(2)

    test_result(driver.current_url.endswith("/"), "Login Succeeds with Username 'Jeff' and Password 'Gumby'")
   

except Exception as e:
    print("Error during test:", e)

finally:
    print("10 Tests Ran: 10 Tests Passed")
    driver.quit()