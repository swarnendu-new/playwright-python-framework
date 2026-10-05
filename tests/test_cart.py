from playwright.sync_api import expect

from pages.login_page import LoginPage
from pages.inventory_page import InventoryPage
from pages.cart_page import CartPage


def test_add_and_remove_product_from_cart(page):
    """
    E2E flow:
    Login → Add Bike Light → Open Cart → Verify product/price → Remove product
    """

    # Arrange: all Page Objects share the same Playwright Page
    login_page = LoginPage(page)
    inventory_page = InventoryPage(page)
    cart_page = CartPage(page)

    product_name = "Sauce Labs Bike Light"
    expected_price = "$9.99"

    # Login
    login_page.open()
    login_page.login("standard_user", "secret_sauce")
    expect(page).to_have_url(InventoryPage.URL)

    # Add product to cart
    inventory_page.add_product_to_cart(product_name)

    expect(inventory_page.cart_badge).to_have_text("1")

    # Open cart
    inventory_page.open_cart()
    expect(page).to_have_url(CartPage.URL)

    # Verify product exists in cart
    cart_item = cart_page.get_cart_item(product_name)
    expect(cart_item).to_be_visible()

    # Verify product price
    actual_price = cart_page.get_product_price(product_name)
    assert actual_price == expected_price

    # Remove product
    cart_page.remove_product(product_name)

    # Verify cart is empty
    assert cart_page.get_cart_item_count() == 0
