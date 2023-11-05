# Please, complete the following task.
# For this site https://www.saucedemo.com/
#  using Selenium Webdriver methods need to create some script with these steps:
#  1. open site (https://www.saucedemo.com/)
#  2. paste correct name into Username field (info below)
#  3. paste correct password into Password field (info below also)
#  4. click to Login button
#  5. get current URL
#  6. check that current URL and expected URL (https://www.saucedemo.com/inventory.html, for example) are the same
# IMPORTANT OBJECTIVE FOR THIS TASK:
# need to use at least 2 different methods for locators search (for example, using DOM and XPath: By.ID for username
# field and By.XPATH for password field)
# CREDENTIALS
# You can find them on the main page. For example these ones:
# standard_user
# secret_sauce
### Dont forget about Selenium and Webdriver
# To install selenium use this command - pip install selenium.
# For local run need to download and install Selenium WebDriver
# (for Google Chrome, for example, you can use this link - https://chromedriver.chromium.org/downloads).
# Major versions of your browser and your webdriver should be the same.
# More info - https://www.browserstack.com/guide/run-selenium-tests-using-selenium-chromedriver
### Review
#  Put me as reviewer please (@VAlexandrov911)
# When you are ready with the task attach it to the "Result" field and change the status for "Needs review"

from selenium import webdriver
from selenium.webdriver.common.by import By

import pytest

class hw12and13_page:
    username_field = (By.ID, "user-name")
    password_field = (By.XPATH, "//input[@placeholder='Password']")
    login_button = (By.CSS_SELECTOR, "input.submit-button.btn_action")

    def __init__(self, driver):
        self.driver = driver

    def open_page(self):
        self.driver.get("https://www.saucedemo.com/")

    def login(self, username, password):
        self.driver.find_element(*self.username_field).send_keys(username)
        self.driver.find_element(*self.password_field).send_keys(password)
        self.driver.find_element(*self.login_button).click()

    def validate_url(self):
        current_url = self.driver.current_url
        expected_url = "https://www.saucedemo.com/inventory.html"
        assert current_url == expected_url


@pytest.fixture
def driver():
    driver = webdriver.Chrome()
    yield driver
    driver.quit()


def test_login(driver):
    login_page = hw12and13_page(driver)
    login_page.open_page()
    login_page.login("standard_user", "secret_sauce")
    login_page.validate_url()
