import os
import time
import unittest
import unittest.mock

from selenium import webdriver
from selenium.common.exceptions import NoSuchElementException
from selenium.webdriver.common.by import By
from selenium.webdriver.chrome.options import Options


YOUFACE_URL = "http://localhost:5000"
VALID_USER = "Jeff"
VALID_PASS = "Jeffy"


class TestLoginPage(unittest.TestCase):

    def setUp(self):
        pass

    def tearDown(self):
        pass


    def test_create_user(self):
        chrome_options = Options()
        chrome_options.add_argument("--no-sandbox")
        chrome_options.add_argument("--headless")
        timestamp = str(int(time.time()))
        user_data_dir = f"--user-data-dir=/tmp/chrome-user-data-{timestamp}"
        chrome_options.add_argument(user_data_dir)

        driver = webdriver.Chrome(options=chrome_options)
        #
        # test empty username and password
        #
        "As a user, if I type in a blank username and password, I should not be able to create a user"
        driver.get(YOUFACE_URL)

        time.sleep(3)

        # try:
        #     create_btn = driver.find_element(By.CLASS_NAME, "btn-success")
        # except NoSuchElementException:
        #     self.fail("Failed to find the create button.")
        # create_btn.click()

        self.assertIn("loginscreen", driver.current_url)

        driver.close()

    # Connor Unit test #
'''class GamesSectionTests(unittest.TestCase):
    def setUp(self):
        opts = Options()
        opts.add_argument("--headless")
        opts.add_argument(f"--user-data-dir=/tmp/chrome-data-{time.time()}")
        self.driver = webdriver.Chrome(options=opts)
        self.driver.implicitly_wait(3)

        self.driver.get(f"{YOUFACE_URL}/loginscreen")
        self.driver.find_element(By.NAME, "username").send_keys(VALID_USER)
        self.driver.find_element(By.NAME, "password").send_keys(VALID_PASS)
        self.driver.find_element(
            By.CSS_SELECTOR, "input[type='submit'][value='Login']"
        ).click()

        self.driver.get(f"{YOUFACE_URL}/games")

    def tearDown(self):
        self.driver.quit()

    def test_games_page_heading(self):
        self.driver.get(f"{YOUFACE_URL}/games")
        heading = self.driver.find_element(By.CSS_SELECTOR, "h2.text-2xl")
        self.assertEqual(heading.text, "Games Section")
        print(f"[PASSED] - {self._testMethodName}")

    def test_games_page_paragraph(self):
        self.driver.get(f"{YOUFACE_URL}/games")
        p = self.driver.find_element(By.CSS_SELECTOR, "div.container p.mb-6")
        self.assertIn("Welcome to the games section", p.text)
        print(f"[PASSED] - {self._testMethodName}")

    def test_plinko_card_link(self):
        self.driver.get(f"{YOUFACE_URL}/games")
        plinko_img = self.driver.find_element(
            By.CSS_SELECTOR, "a[href='/plinko'] img[alt='Plinko']"
        )
        self.assertTrue(plinko_img.is_displayed())
        print(f"[PASSED] - {self._testMethodName}")

    def test_blackjack_card_link(self):
        self.driver.get(f"{YOUFACE_URL}/games")
        bj_img = self.driver.find_element(
            By.CSS_SELECTOR, "a[href='/blackjack'] img[alt='Blackjack']"
        )
        self.assertTrue(bj_img.is_displayed())
        print(f"[PASSED] - {self._testMethodName}")


class PlinkoTests(unittest.TestCase):
    def setUp(self):
        opts = Options()
        opts.add_argument("--headless")
        opts.add_argument(f"--user-data-dir=/tmp/chrome-data-{time.time()}")
        self.driver = webdriver.Chrome(options=opts)
        self.driver.get(f"{YOUFACE_URL}/plinko")
        self.driver.implicitly_wait(3)

        self.driver.get(f"{YOUFACE_URL}/loginscreen")
        self.driver.find_element(By.NAME, "username").send_keys(VALID_USER)
        self.driver.find_element(By.NAME, "password").send_keys(VALID_PASS)
        self.driver.find_element(
            By.CSS_SELECTOR, "input[type='submit'][value='Login']"
        ).click()

        self.driver.get(f"{YOUFACE_URL}/plinko")
    def tearDown(self):
        self.driver.quit()

    def test_plinko_modal_visible_on_load(self):
        modal = self.driver.find_element(By.ID, "plinkoModal")
        self.assertTrue(modal.is_displayed())
        print(f"[PASSED] - {self._testMethodName}")

    def test_plinko_close_modal(self):
        close_btn = self.driver.find_element(By.CSS_SELECTOR, "#plinkoModal .close")
        close_btn.click()
        modal = self.driver.find_element(By.ID, "plinkoModal")
        self.assertEqual(modal.value_of_css_property("display"), "none")
        print(f"[PASSED] - {self._testMethodName}")

    def test_drop_button_exists(self):
        drop_btn = self.driver.find_element(By.ID, "drop-button")
        self.assertTrue(drop_btn.is_enabled())
        print(f"[PASSED] - {self._testMethodName}")

    def test_multiplier_initial_value(self):
        m = self.driver.find_element(By.ID, "multiplier")
        self.assertEqual(m.text, "1")
        print(f"[PASSED] - {self._testMethodName}")


class BlackjackTests(unittest.TestCase):
    def setUp(self):
        opts = Options()
        opts.add_argument("--headless")
        opts.add_argument(f"--user-data-dir=/tmp/chrome-data-{time.time()}")
        self.driver = webdriver.Chrome(options=opts)
        self.driver.get(f"{YOUFACE_URL}/blackjack")
        self.driver.implicitly_wait(3)

        self.driver.get(f"{YOUFACE_URL}/loginscreen")
        self.driver.find_element(By.NAME, "username").send_keys(VALID_USER)
        self.driver.find_element(By.NAME, "password").send_keys(VALID_PASS)
        self.driver.find_element(
            By.CSS_SELECTOR, "input[type='submit'][value='Login']"
        ).click()

        self.driver.get(f"{YOUFACE_URL}/blackjack")

    def tearDown(self):
        self.driver.quit()

    def test_blackjack_buttons_exist(self):
        for btn_id in ("deal-button", "hit-button", "stand-button"):
            btn = self.driver.find_element(By.ID, btn_id)
            self.assertTrue(btn.is_enabled())
        print(f"[PASSED] - {self._testMethodName}")

    def test_deal_creates_cards(self):
        self.driver.find_element(By.CSS_SELECTOR, "#rulesModal .close").click()
        self.driver.find_element(By.ID, "deal-button").click()
        time.sleep(1)
        player = self.driver.find_elements(By.CSS_SELECTOR, "#player-hand .card")
        dealer = self.driver.find_elements(By.CSS_SELECTOR, "#dealer-hand .card")
        self.assertEqual(len(player), 2)
        self.assertEqual(len(dealer), 2)
        print(f"[PASSED] - {self._testMethodName}")

    def test_hit_adds_card(self):
        self.driver.find_element(By.CSS_SELECTOR, "#rulesModal .close").click()
        self.driver.find_element(By.ID, "deal-button").click()
        time.sleep(1)
        before = len(self.driver.find_elements(By.CSS_SELECTOR, "#player-hand .card"))
        self.driver.find_element(By.ID, "hit-button").click()
        time.sleep(1)
        after = len(self.driver.find_elements(By.CSS_SELECTOR, "#player-hand .card"))
        self.assertEqual(after, before + 1)
        print(f"[PASSED] - {self._testMethodName}")

    def test_rules_modal_close(self):
        modal = self.driver.find_element(By.ID, "rulesModal")
        self.assertTrue(modal.is_displayed())
        self.driver.find_element(By.CSS_SELECTOR, "#rulesModal .close").click()
        modal = self.driver.find_element(By.ID, "rulesModal")
        self.assertEqual(modal.value_of_css_property("display"), "none")
        print(f"[PASSED] - {self._testMethodName}")

if __name__ == "__main__":
    unittest.main()
'''