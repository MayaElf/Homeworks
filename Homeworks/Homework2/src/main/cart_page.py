from selenium.webdriver.common.by import By
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.support.wait import WebDriverWait

class CartPage:
    cart_item_name = (By.CSS_SELECTOR, "#tbodyid td:nth-of-type(2)")
    cart_item_price = (By.CSS_SELECTOR, "#tbodyid td:nth-of-type(3)")

    def __init__(self, driver):
        self.driver = driver
        self.wait = WebDriverWait(self.driver, 3)

    def verify_item_to_cart(self, current_item_name, current_item_price):
        original_item_name = self.wait.until(EC.visibility_of_element_located(self.cart_item_name))
        assert original_item_name.text == current_item_name
        original_item_price = self.driver.find_element(*self.cart_item_price)
        assert float(original_item_price.text) == float(current_item_price)
