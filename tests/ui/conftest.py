import pytest

from pages.cart_page import CartPage
from pages.inventory_page import InventoryPage
from pages.login_page import LoginPage
from utils.config_loader import AppConfig


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
