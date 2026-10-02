import pytest
import logging

from pages.cart_page import CartPage
from pages.inventory_page import InventoryPage
from pages.login_page import LoginPage

from utils.config_loader import load_config
from utils.config_loader import AppConfig
from utils.logging_config import configure_logging

@pytest.fixture(scope="session", autouse=True)
def set_configure(worker_id):
    configure_logging(worker_id)

test_logger = logging.getLogger("test")

def pytest_runtest_logstart(nodeid, location):
    test_logger.info("=" * 80)
    test_logger.info("START: %s", nodeid)

def pytest_runtest_logreport(report):
    if report.when == "call":

        if report.passed:
            test_logger.info(
                "%s: %s (%.fs)",
                report.outcome.upper(),
                report.nodeid,
                report.duration
            )

        elif report.failed:
            test_logger.error(
                "FAILED: %s (%.fs)",
                report.nodeid,
                report.duration
            )
        elif report.skipped:
            test_logger.warning(
                "SKIPPED: %s",
                report.nodeid
            )

    elif report.failed:
        test_logger.error(
            "FAILED: %s: %s (%.fs)",
            report.when,
            report.nodeid,
            report.duration
        )


def pytest_addoption(parser):
    parser.addoption(
        "--env",
        action="store",
        default="qa",
        help="Test environment",
    )

@pytest.fixture(scope="session")
def app_config(request) -> AppConfig:
    environment = request.config.getoption("--env")

    return load_config(environment)

# @pytest.fixture(scope="session", autouse=True)
# def show_config(app_config):
#     print("\n CONFIG:")
#     print(app_config)

@pytest.fixture(autouse=True)
def configure_page(page, app_config: AppConfig):
    page.set_default_timeout(
        app_config.browser.timeout
    )

@pytest.fixture
def numbers():
    print("\nSETUP: prepare test data")

    a = 10
    b = 5

    yield a, b

    print("\nTEARDOWN: clean up test data")

@pytest.fixture
def calculation_data(numbers):
    a, b = numbers

    return {
        "a": a,
        "b": b,
        "expected_sum": 15,
        "expected_difference": 5,
    }

@pytest.fixture
def multiplication_data(numbers):
    a, b = numbers

    return {
        "a": a,
        "b": b,
        "expected_multiply": 50
    }


@pytest.fixture
def login_page(page, app_config):
    return LoginPage(page, app_config.base_url)


@pytest.fixture
def inventory_page(page, app_config):
    return InventoryPage(page, app_config.base_url)

@pytest.fixture
def cart_page(page, app_config):
    return CartPage(page, app_config.base_url)

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