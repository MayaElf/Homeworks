import time

from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.support.wait import WebDriverWait

class DemoBlazePage:
    user_name = (By.ID, "loginusername")
    user_password = (By.ID, "loginpassword")
    login_button = (By.ID, "login2")
    login_text_button = (By.XPATH, "//button[contains(text(),'Log in')]")
    logout_button = (By.ID, "logout2")
    welcome_message = (By.ID, "nameofuser")

    monitors_button = (By.LINK_TEXT, "Monitors")

    def __init__(self, driver):
        self.driver = driver
        self.wait = WebDriverWait(self.driver, 3)

    def chrome_driver(self):
        self.driver = webdriver.Chrome()

    def open_url(self):
        self.driver.get("https://www.demoblaze.com/")

    def click_login_button(self):
        self.driver.find_element(*self.login_button).click()

    def setup_login_and_password(self, userlogin, password):
        self.wait.until(EC.visibility_of_element_located(self.user_name)).send_keys(userlogin)

        self.driver.find_element(*self.user_password).send_keys(password)
        self.driver.find_element(*self.login_text_button).click()
        time.sleep(3)

    def verify_login(self, login):
        self.wait.until(EC.visibility_of_element_located(self.welcome_message))
        welcome_message = self.driver.find_element(*self.welcome_message).text
        assert welcome_message == f"Welcome {login}"

    def click_monitors_button(self):
        self.driver.find_element(*self.monitors_button).click()

    def select_high_price_item(self):
        monitor_items = self.driver.find_elements(By.CLASS_NAME, "card-block")
        time.sleep(3)

        items = []

        for monitor in monitor_items:
            element = self.wait.until(EC.presence_of_element_located((By.CLASS_NAME, "card-title")))

            title = self.wait.until(EC.presence_of_element_located((By.CLASS_NAME, "card-title"))).text
            # price_element = monitor.find_element(By.TAG_NAME, "h5")
            price_element = self.wait.until(EC.presence_of_element_located((By.XPATH, "//*[contains(text(),'$')]")))
            price = float(price_element.text.split("$")[1])
            items.append((title, price))

        sorted_items = sorted(items, key=lambda x: x[1], reverse=True)
        high_price_item = sorted_items[0]

        return high_price_item

    def click_high_price_item(self, item):
        self.driver.find_element(By.XPATH, f"//a[contains(.,'{item[0]}')]").click()
