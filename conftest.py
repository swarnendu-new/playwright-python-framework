import pytest
from playwright.sync_api import sync_playwright
"""
conftest.py is automatically discovered by pytest and is used to define
shared fixtures/setup/teardown that can be reused across test files
without importing them explicitly.

Here, the page fixture manages the Playwright browser lifecycle:
start Playwright → launch browser → create context/page → run test → cleanup.
"""
'''
pytest -> fixture
function → once per test function       ← current/default
class    → once per test class
module   → once per test file/module
session  → once for entire test run
'''


@pytest.fixture(scope="function")
def page():
    """Create fresh playwright page for each test"""

    playwright = sync_playwright().start()  # start playwright
    browser = playwright.chromium.launch(headless=False)  # launch browser
    context = browser.new_context()  # create isolated browser session
    page = context.new_page()  # Open new page

    yield page  # Give the page to the test

    context.close()  # Clean up browser context after test
    browser.close()  # Close browser
    playwright.stop()  # Stop Playwright
