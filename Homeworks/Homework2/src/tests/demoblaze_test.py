from Homeworks.Homework2.src.main.config import user_name, user_password


class TestDemoBlaze:
    # Test: login
    def test_login(self, demo_blaze_page):
        demo_blaze_page.click_login_button()
        demo_blaze_page.setup_login_and_password(user_name, user_password)
        demo_blaze_page.verify_login(user_name)

    # Test: add to cart
    def test_add_to_cart(self, demo_blaze_page, item_page, cart_page):

        # Step 1: Login
        demo_blaze_page.click_login_button()
        demo_blaze_page.setup_login_and_password(user_name, user_password)

        # Step 2: Go to monitors page
        demo_blaze_page.click_monitors_button()

        # Step 3: Choose item with the highest price
        high_price_item = demo_blaze_page.select_high_price_item()

        # Step 4: Go to item page and check item info
        demo_blaze_page.click_high_price_item(high_price_item)
        item_page.item_verify(high_price_item[0], f"${high_price_item[1]}")

        # Step 5: Add item to cart and check
        item_page.add_item_to_cart()
        item_page.click_to_cart_button()
        cart_page.verify_item_to_cart(high_price_item[0], f"{high_price_item[1]}")
