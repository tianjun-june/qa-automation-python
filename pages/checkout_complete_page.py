import logging

from playwright.sync_api import Page,expect


logger = logging.getLogger(__name__)

class CheckoutCompletePage:

    def __init__(self, page:Page):
        self.page = page

        self.title = self.page.get_by_test_id("title")
        self.generate_pdf_order_button = self.page.get_by_test_id("generate-pdf-order")

    def open(self):
        self.page.goto("checkout-complete.html")

    def verify_checkout_complete_is_loaded(self):
        expect(self.title).to_have_text("Checkout: Complete!")

    def generate_pdf_order(self):
        logger.info(f"Generating PDF order")
        self.generate_pdf_order_button.click()