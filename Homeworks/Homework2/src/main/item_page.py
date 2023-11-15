from selenium.webdriver.common.by import By
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.support.wait import WebDriverWait

class ItemPage():
    item_name = (By.CLASS_NAME, "name")
    item_price = (By.CSS_SELECTOR, "h3.price-container")

    add_to_cart = (By.XPATH, "//a[contains(text(),'Add to cart')]")
    cart_button = (By.ID, "cartur")

    def __init__(self, driver):
        self.driver = driver
        self.wait = WebDriverWait(self.driver, 3)

    def item_verify(self, current_item_name, current_item_price):
        self.wait.until(EC.visibility_of_element_located(self.item_name))

        original_item_name = self.driver.find_element(*self.item_name).text
        assert original_item_name == current_item_name
        original_item_price = self.driver.find_element(*self.item_price).text.split('*')[0].strip()
        assert original_item_price in current_item_price

    def add_item_to_cart(self):
        self.driver.find_element(*self.add_to_cart).click()
        alert = self.wait.until(EC.alert_is_present())
        alert.accept()

    def click_to_cart_button(self):
        self.wait.until(EC.visibility_of_element_located(self.cart_button))
        self.driver.find_element(*self.cart_button).click()
