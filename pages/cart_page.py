import re
from playwright.sync_api import Page, expect

class CartPage:

    # URL = f"{BASE_URL}/cart.html"

    def __init__(self, page: Page):
        self.page = page

        self.cart_items = page.locator(".cart_item")
        self.item_names = page.locator(".inventory_item_name")

    def verify_loaded(self):
        expect(self.page).to_have_url(re.compile(r".*/cart\.html$"))

    def get_item_names(self):
        return self.item_names.all_text_contents()
