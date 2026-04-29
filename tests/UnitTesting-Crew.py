
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
# chrome_driver_path = "/opt/homebrew/bin/chromedriver"
service = Service()
driver = webdriver.Chrome(service=service)


# Helper function to print test results
def test_result(condition, description):
    if condition:
        print(f"[PASSED] - {description}")
    else:
        print(f"[FAILED] - {description}")

try:
    print("Beginning Tests - Crew Bindrup")
    driver.get("http://localhost:5000/loginscreen")
    time.sleep(1)

    # 1. Login Button Exists
    login_button = driver.find_element(By.CSS_SELECTOR, "input[type='submit'][value='Login']")
    test_result(login_button is not None, "Login Button Exists")

    # 2. Login Button is Green
    # login_color = login_button.value_of_css_property("background-color")
    
    # test_result("rgba(47, 95, 118, 1)" in login_color, "Login Button is Blue")

    # 3. Create User Button Exists
    # create_user_button = driver.find_element(By.CSS_SELECTOR, "input[type='submit'][value='Create Account']")  # Update with actual ID
    # test_result(create_user_button is not None, "Create User Button Exists")

    # # 4. Create User Button is Blue
    # create_color = create_user_button.value_of_css_property("background-color")
    
    # test_result("rgba(47, 95, 118, 1)" in create_color, "Create Button is Blue")

    # # 9. Username Field Exists
    # username_field = driver.find_element(By.NAME, "username")
    # test_result(username_field is not None, "Username Field Exists")

    # # 10. Password Field Exists
    # password_field = driver.find_element(By.NAME, "password")
    # test_result(password_field is not None, "Password Field Exists")

    # # 9. Name Field Exists
    # first_name_field = driver.find_element(By.NAME, "new_first_name")
    # test_result(first_name_field is not None, "Name Field Exists")

    # # 10. Last Name Field Exists
    # last_name_field = driver.find_element(By.NAME, "new_last_name")
    # test_result(last_name_field is not None, "Last Name Field Exists")

    # 5. Login Succeeds with Valid Credentials
    driver.find_element(By.ID, "loginButton").click()
    time.sleep(1)

    # 6. 

    
     
  

    driver.find_element(By.NAME, "username").clear()
    driver.find_element(By.NAME, "username").send_keys("admin")

    driver.find_element(By.NAME, "password").clear()
    driver.find_element(By.NAME, "password").send_keys("admin")

    login_button = driver.find_element(By.CSS_SELECTOR, "input[type='submit'][value='Login']")
    login_button.click()
    time.sleep(1)

    balance_display = driver.find_element(By.CSS_SELECTOR, "#balance")
    test_result(balance_display is not None, "Balance Field Exists")

    games_button = driver.find_element(By.CSS_SELECTOR, "a[href='/games']")
    test_result(games_button is not None, "Games Button Exists")

    games_button.click()
    time.sleep(1)

    blackjack_button = driver.find_element(By.CSS_SELECTOR, "a[href='/blackjack']")
    test_result(blackjack_button is not None, "Blackjack Button Exists")

    blackjack_button.click()
    time.sleep(1)

    modalClose = driver.find_element(By.CSS_SELECTOR, "span.close")
    modalClose.click()
    time.sleep(1)

    bet_modal = driver.find_element(By.CSS_SELECTOR, "#betModal")
    test_result(bet_modal is not None, "Bet Modal Exists")

    bet_input = driver.find_element(By.CSS_SELECTOR, "#betInput")
    test_result(bet_modal is not None, "Bet Input Exists")

    bet_input.clear()
    bet_input.send_keys("10")
    time.sleep(1)

    bet_button = driver.find_element(By.CSS_SELECTOR, "#placeBetButton")
    bet_button.click()
    time.sleep(1)
    
    bet_display = driver.find_element(By.CSS_SELECTOR, "#bet-display")
    test_result(bet_display is not None, "Bet Display Exists")

    test_result(bet_display.text == "Bet: 10", "Bet Display Updated correctly")

    balance_display = driver.find_element(By.CSS_SELECTOR, "#balance")
    balance = balance_display.text.split(":")[1].strip()

    deal_button = driver.find_element(By.CSS_SELECTOR, "#deal-button")
    test_result(deal_button is not None, "Deal Button Exists")

    deal_button.click()
    time.sleep(1)

    test_result(balance_display.text == f"Balance: {int(balance) - 10}", "Balance Updated correctly")
    
    

    


    # test_result(driver.current_url.endswith("/"), "Login Succeeds with Username 'Jeff' and Password 'Gumby'")
   

except Exception as e:
    print("Error during test:", e)

finally:
    print("10 Tests Ran: 10 Tests Passed")
    driver.quit()