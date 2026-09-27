import logging
from playwright.sync_api import Page


logger = logging.getLogger(__name__)

class LoginPage:

    def __init__(self, page: Page, base_url:str):
        self.page = page
        self.url = f"{base_url}/"

        self.username_input = page.get_by_placeholder("username")
        self.password_input = page.get_by_placeholder("password")
        self.login_button = page.get_by_role("button", name='Login')
        self.error_message = page.locator('[data-test="error"]')

    def open(self):
        logger.info("Opening login page: %s", self.url)
        self.page.goto(self.url)

    def login(self, username: str, password: str):
        logger.info("Logging in as user: %s", username)

        self.username_input.fill(username)
        self.password_input.fill(password)
        self.login_button.click()