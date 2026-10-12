import logging

import pytest
from pathlib import Path

from playwright.sync_api import Browser, Playwright

from pytest_playwright.pytest_playwright import CreateContextCallback
from pages.cart_page import CartPage
from pages.checkout_complete_page import CheckoutCompletePage
from pages.checkout_step_two_page import CheckoutStepTwoPage
from pages.inventory_page import InventoryPage
from pages.login_page import LoginPage
from utils.config_loader import AppConfig


logger = logging.getLogger(__name__)

@pytest.fixture(scope="session", autouse=True)
def configure_test_id_attribute(playwright: Playwright):
    playwright.selectors.set_test_id_attribute("data-test")

@pytest.fixture
def login_page(page):
    return LoginPage(page)


@pytest.fixture
def inventory_page(page):
    return InventoryPage(page)

@pytest.fixture
def cart_page(page):
    return CartPage(page)

@pytest.fixture
def logged_in_inventory_page(
        login_page,
        inventory_page,
        app_config,
):
    credentials = app_config.credentials
    login_page.open()
    login_page.login(credentials.username, credentials.password)

    inventory_page.verify_loaded()

    return inventory_page

@pytest.fixture(autouse=True)
def configure_context(context, app_config: AppConfig):
    context.set_default_timeout(
        app_config.browser.timeout
    )

@pytest.fixture(scope="session")
def browser_context_args(
        browser_context_args,
        app_config,
):
    return {
        **browser_context_args,
        "base_url": app_config.base_url,
    }

@pytest.fixture(scope="session")
def auth_storage_state(
        browser:Browser,
        app_config:AppConfig,
        tmp_path_factory,
) -> Path:
    auth_dir = tmp_path_factory.mktemp("auth")
    auth_file = auth_dir / "user.json"

    context = browser.new_context(
        base_url=app_config.base_url,
    )
    page = context.new_page()

    login_page = LoginPage(page)

    login_page.open()

    login_page.login(app_config.credentials.username,
                     app_config.credentials.password)

    context.storage_state(
        path=auth_file
    )
    logger.info("created auth storage state",)
    context.close()

    return auth_file

# This can add another BrowserContext
# @pytest.fixture
# def authenticated_context(
#         browser,
#         browser_context_args,
#         auth_storage_state,
# ):
#     context = browser.new_context(
#         **browser_context_args,
#         storage_state=auth_storage_state,
#     )
#
#     yield context
#
#     context.close()
#
# @pytest.fixture
# def authenticated_page(
#         authenticated_context,
# ):
#     page = authenticated_context.new_page()
#
#     yield page
#
#     page.close()

@pytest.fixture
def authenticated_page(
        new_context: CreateContextCallback,
        auth_storage_state: Path,
):
    context = new_context(
        storage_state=auth_storage_state,
    )
    return context.new_page()

@pytest.fixture
def authenticated_inventory_page(
        authenticated_page
):
    return InventoryPage(authenticated_page)

@pytest.fixture
def authenticated_checkout_step_two_page(authenticated_page):
    return CheckoutStepTwoPage(authenticated_page)

@pytest.fixture
def authenticated_checkout_complete_page(authenticated_page):
    return CheckoutCompletePage(authenticated_page)

