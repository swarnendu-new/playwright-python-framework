from playwright.sync_api import expect

from pages.login_page import LoginPage
from pages.inventory_page import InventoryPage


def test_product_price(page):
    """Verify Bike Light displays the expected price after login."""

    # Arrange: create Page Objects using the same Playwright page
    login_page = LoginPage(page)
    inventory_page = InventoryPage(page)

    # Act: login to the application
    login_page.open()
    login_page.login("standard_user", "secret_sauce")

    # Assert: verify successful navigation to Inventory page
    expect(page).to_have_url(InventoryPage.URL)

    # Act: get product price through InventoryPage
    actual_price = inventory_page.get_product_price(
        "Sauce Labs Bike Light"
    )

    # Assert: verify returned Python value
    assert actual_price == "$9.99"

    print("PASS: Bike Light price is $9.99")
