from playwright.sync_api import Page

"""
    Page Object Model (POM) for the SauceDemo Inventory page.

    Responsibilities:
    - Stores page-level locators such as products, sort dropdown, and cart.
    - Finds dynamic/repeated products by product name instead of index.
    - Provides reusable actions such as sorting, adding products to cart,
      reading product prices, and opening the cart.
    - Accepts test data such as product_name instead of hardcoding products.

"""


class InventoryPage:
    """Page Object for the SauceDemo inventory/products page."""

    URL = "https://www.saucedemo.com/inventory.html"

    def __init__(self, page: Page):
        self.page = page

        # Page-level locators
        self.products = page.locator(".inventory_item")
        self.sort_dropdown = page.locator(
            "[data-test='product-sort-container']"
        )
        self.cart_badge = page.locator(".shopping_cart_badge")
        self.cart_link = page.locator(".shopping_cart_link")

    def get_product(self, product_name: str):
        """Return the product container matching the given product name."""
        return self.products.filter(has_text=product_name)

    def get_product_price(self, product_name: str):
        """Return the displayed price text for a product."""
        product = self.get_product(product_name)
        return product.locator(".inventory_item_price").inner_text()

    def add_product_to_cart(self, product_name: str):
        """Add the specified product to the cart."""
        product = self.get_product(product_name)
        product.get_by_role("button", name="Add to cart").click()

    def sort_products(self, option: str):
        """Sort products using the dropdown option value."""
        self.sort_dropdown.select_option(option)

    def open_cart(self):
        """Open the shopping cart."""
        self.cart_link.click()
