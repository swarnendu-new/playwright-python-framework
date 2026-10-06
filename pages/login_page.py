from playwright.sync_api import Page


class LoginPage:
    """
    Page object for the saucedemo login page
    Encapsulates login-page locators and reusable actions so tests
    describe WHAT to validate while the Page Object handles HOW
    to interact with the UI.
    """

    URL = "https://www.saucedemo.com/"

    def __init__(self, page: Page):
        self.page = page

        # Locators belonging to the login page
        self.username = page.locator("[data-test='username']")
        self.password = page.get_by_placeholder("Password")
        self.login_button = page.get_by_role("button", name="Login")

    def open(self):
        """Open the Sauce demo login page"""
        self.page.goto(self.URL)

    def login(self, username: str, password: str):
        """Login using supplied credential"""
        self.username.fill(username)
        self.password.fill(password)
        self.login_button.click()

    def get_error_message(self):
        """Return the login error message displayed after an unsuccessful login."""
        return self.page.locator("[data-test='error']").inner_text()
