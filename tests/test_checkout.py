from playwright.sync_api import expect

from pages.login_page import LoginPage
from pages.inventory_page import InventoryPage
from pages.cart_page import CartPage
from pages.checkout_page import CheckoutPage


def test_complete_checkout(page):
    """
    Verify a customer can complete the full purchase flow.

    Flow:
    Login → Add product → Cart → Checkout → Customer info
    → Order overview → Finish → Order confirmation
    """

    login_page = LoginPage(page)
    inventory_page = InventoryPage(page)
    cart_page = CartPage(page)
    checkout_page = CheckoutPage(page)

    # Test data belongs in the test, not inside the Page Objects.
    product_name = "Sauce Labs Bike Light"

    # Login
    login_page.open()
    login_page.login("standard_user", "secret_sauce")
    expect(page).to_have_url(InventoryPage.URL)

    # Add product and verify the cart is updated.
    inventory_page.add_product_to_cart(product_name)
    expect(inventory_page.cart_badge).to_have_text("1")

    # Open cart and verify the selected product is present.
    inventory_page.open_cart()
    expect(page).to_have_url(CartPage.URL)

    cart_item = cart_page.get_cart_item(product_name)
    expect(cart_item).to_be_visible()

    # Proceed to checkout.
    cart_page.proceed_to_checkout()
    expect(page).to_have_url(CheckoutPage.INFO_URL)

    # Enter customer information.
    checkout_page.enter_customer_information(
        first_name="John",
        last_name="Doe",
        postal_code="98034",
    )

    checkout_page.continue_checkout()

    # Verify customer information submission navigates to order overview.
    expect(page).to_have_url(CheckoutPage.OVERVIEW_URL)

    # Complete the order.
    checkout_page.finish_order()

    # Verify navigation and successful order confirmation.
    expect(page).to_have_url(CheckoutPage.COMPLETE_URL)
    expect(checkout_page.complete_header).to_have_text(
        "Thank you for your order!"
    )
