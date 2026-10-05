from playwright.sync_api import expect
from pages.login_page import LoginPage


def test_valid_login(page):
    """Verify a user can log in with valid credentials."""

    login_page = LoginPage(page)  # Pass pytest-created Page to the Page Object

    login_page.open()  # navigate to source demo
    login_page.login("standard_user", "secret_sauce")  # perform login

    # Verify successful login
    expect(page).to_have_url("https://www.saucedemo.com/inventory.html")
