from playwright.sync_api import Page,expect
import logging

logger = logging.getLogger(__name__)


class CheckoutStepTwoPage:
    def __init__(self, page: Page):
        self.page = page

        self.title = page.get_by_test_id("title")
        self.finish_button = page.get_by_role("button", name="Finish")

    def open(self):
        self.page.goto("/checkout-step-two.html")

    def verify_checkout_step_two_is_loaded(self):
        expect(self.title).to_have_text("Checkout: Overview")

    def finish_checkout(self):
        logger.info("Finish checkout, go to next page.")
        self.finish_button.click()
