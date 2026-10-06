import pytest
from pathlib import Path
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


def pytest_addoption(parser):
    """
    Adding custom command-line options for test execution.

    --browser selects the Playwright browser.
    --headed displays the browser UI during execution.
    """

    parser.addoption(
        "--browser",
        action="store",
        default="chromium",
        choices=["chromium", "chrome", "firefox", "webkit"],
        help="Browser to run tests: chromium, chrome, firefox, or webkit",
    )

    parser.addoption(
        "--headed",
        action="store_true",
        default=False,
        help="Run browser in headed mode",
    )


@pytest.hookimpl(hookwrapper=True)
def pytest_runtest_makereport(item, call):
    """
    Store the pytest result for each test phase.

    This allows fixtures to determine whether a test passed or failed
    and perform failure-specific actions such as taking screenshots.
    """
    outcome = yield
    report = outcome.get_result()

    setattr(item, f"rep_{report.when}", report)


@pytest.fixture
def page(request):
    """
    Create a fresh Playwright page for each test.

    Browser type and headed/headless mode are controlled through
    pytest command-line options.
    """

    # Read custom command-line options defined in pytest_addoption().
    browser_name = request.config.getoption("--browser")
    headed = request.config.getoption("--headed")

    playwright = sync_playwright().start()

    # Dynamically select chromium, firefox, or webkit.
    # Playwright expects headless=True to hide the browser.
    # Therefore --headed reverses the headless value.
    # Chrome is a branded Chromium browser and is launched using a channel.
    if browser_name == "chrome":
        browser = playwright.chromium.launch(
            channel="chrome",
            headless=not headed,
        )
    else:
        # Chromium, Firefox, and WebKit map directly to Playwright browser types.
        browser_type = getattr(playwright, browser_name)
        browser = browser_type.launch(headless=not headed)

    context = browser.new_context()
    page = context.new_page()

    # Test execution pauses here and receives the Page object.
    yield page

    print("DEBUG: returned to fixture after test")

    # Capture a screenshot automatically when the test itself fails.
    if hasattr(request.node, "rep_call") and request.node.rep_call.failed:

        # Create the screenshots directory if it does not already exist.
        screenshot_dir = Path("test-results/screenshots")
        screenshot_dir.mkdir(parents=True, exist_ok=True)

        # Use the pytest test name as the screenshot filename.
        screenshot_path = screenshot_dir / f"{request.node.name}.png"

        page.screenshot(
            path=str(screenshot_path),
            full_page=True,
        )

        print(f"\nFailure screenshot saved: {screenshot_path}")

    # Normal browser cleanup.
    context.close()
    browser.close()
    playwright.stop()
