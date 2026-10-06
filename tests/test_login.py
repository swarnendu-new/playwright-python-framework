import pytest
from playwright.sync_api import expect

from pages.login_page import LoginPage
from pages.inventory_page import InventoryPage


# Parametrization runs the same test once for each dataset below.
# Each tuple maps to: username → password → expected_url.
# This avoids duplicating test methods for different login users.

@pytest.mark.parametrize(
    "username,password,expected_url",
    [
        ("standard_user", "secret_sauce", InventoryPage.URL),
        ("problem_user", "secret_sauce", InventoryPage.URL),
    ],
)
def test_valid_login(page, username, password, expected_url):
    """
    Verify multiple valid users can log in successfully.

    'page' is injected by the pytest fixture from conftest.py.
    username/password/expected_url are injected by @pytest.mark.parametrize.
    """

    # Page Object receives the Playwright Page created by the pytest fixture.
    login_page = LoginPage(page)

    # Perform login using reusable actions defined in LoginPage.
    login_page.open()
    login_page.login(username, password)

    # Playwright expect() auto-retries until URL matches or timeout occurs.
    expect(page).to_have_url(expected_url)
