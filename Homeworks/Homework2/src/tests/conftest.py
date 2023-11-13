import pytest
from selenium import webdriver

from Homeworks.Homework2.src.main.cart_page import CartPage
from Homeworks.Homework2.src.main.demoblaze_page import DemoBlazePage
from Homeworks.Homework2.src.main.item_page import ItemPage


# To initialize WebDriver
@pytest.fixture
def driver():
    driver = webdriver.Chrome()
    driver.implicitly_wait(10)
    yield driver
    driver.quit()


# To initialize DemoBlaze page
@pytest.fixture
def demo_blaze_page(driver):
    page = DemoBlazePage(driver)
    page.open_url()
    yield page


# To initialize page with item
@pytest.fixture
def item_page(driver):
    page = ItemPage(driver)
    yield page


# To initialize page with cart
@pytest.fixture
def cart_page(driver):
    page = CartPage(driver)
    yield page
