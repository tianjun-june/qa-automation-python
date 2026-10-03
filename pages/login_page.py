import logging
from playwright.sync_api import Page, expect

logger = logging.getLogger(__name__)

class LoginPage:

    def __init__(self, page: Page):
        self.page = page

        self.username_input = page.get_by_placeholder("username")
        self.password_input = page.get_by_placeholder("password")
        self.login_button = page.get_by_role("button", name='Login')
        self.error_message = page.locator('[data-test="error"]')

    def open(self) -> None:
        logger.info("Opening login page", )
        self.page.goto('/')

    def login(self, username: str, password: str) -> None:
        logger.info("Logging in as user: %s", username)

        self.username_input.fill(username)
        self.password_input.fill(password)
        self.login_button.click()

    def verify_error_message(self, expected_message: str) -> None:
        expect(self.error_message).to_be(expected_message)