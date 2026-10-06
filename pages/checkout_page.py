from playwright.sync_api import Page


class CheckoutPage:
    """
    Page Object Model for the SauceDemo checkout flow.

    Handles checkout-specific elements and actions including customer
    information, order completion, and confirmation.
    """

    INFO_URL = "https://www.saucedemo.com/checkout-step-one.html"
    OVERVIEW_URL = "https://www.saucedemo.com/checkout-step-two.html"
    COMPLETE_URL = "https://www.saucedemo.com/checkout-complete.html"

    def __init__(self, page: Page):
        self.page = page

        # Customer information
        self.first_name = page.locator("[data-test='firstName']")
        self.last_name = page.locator("[data-test='lastName']")
        self.postal_code = page.locator("[data-test='postalCode']")

        # Checkout actions
        self.continue_button = page.locator("[data-test='continue']")
        self.finish_button = page.locator("[data-test='finish']")

        # Order confirmation
        self.complete_header = page.locator("[data-test='complete-header']")

    def enter_customer_information(
        self,
        first_name: str,
        last_name: str,
        postal_code: str,
    ):
        """Enter customer information required for checkout."""
        self.first_name.fill(first_name)
        self.last_name.fill(last_name)
        self.postal_code.fill(postal_code)

    def continue_checkout(self):
        """Continue from customer information to checkout overview."""
        self.continue_button.click()

    def finish_order(self):
        """Complete the order from the checkout overview page."""
        self.finish_button.click()
