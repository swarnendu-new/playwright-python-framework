from playwright.sync_api import Page


class CartPage:
    """
    Page Object Model for the SauceDemo Cart page.

    Encapsulates cart-specific locators and reusable actions.
    Tests decide WHAT product/cart behavior to validate; this class
    handles HOW the cart UI is located and interacted with.
    """

    URL = "https://www.saucedemo.com/cart.html"

    def __init__(self, page: Page):
        self.page = page
        self.cart_items = page.locator(".cart_item")
        self.checkout_button = page.locator("[data-test='checkout']")

    def get_cart_item(self, product_name: str):
        """Return the cart item containing the specified product."""
        return self.cart_items.filter(has_text=product_name)

    def get_product_price(self, product_name: str):
        """Return the displayed price for a product in the cart."""
        cart_item = self.get_cart_item(product_name)
        return cart_item.locator(".inventory_item_price").inner_text()

    def remove_product(self, product_name: str):
        """Remove the specified product from the cart."""
        cart_item = self.get_cart_item(product_name)
        cart_item.get_by_role("button", name="Remove").click()

    def get_cart_item_count(self):
        """Return the number of products currently displayed in the cart."""
        return self.cart_items.count()

    def proceed_to_checkout(self):
        """Proceed from the shopping cart to checkout."""
        self.checkout_button.click()
