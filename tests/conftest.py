import pytest
import logging

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

@pytest.fixture(autouse=True)
def configure_page(page, app_config: AppConfig):
    page.set_default_timeout(
        app_config.browser.timeout
    )

