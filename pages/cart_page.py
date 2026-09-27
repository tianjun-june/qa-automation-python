from playwright.sync_api import Page, expect

class CartPage:

    # URL = f"{BASE_URL}/cart.html"

    def __init__(self, page: Page, base_url: str):
        self.page = page
        self.url = f"{base_url}/cart.html"

        self.cart_items = page.locator(".cart_item")
        self.item_names = page.locator(".inventory_item_name")

    def verify_loaded(self):
        expect(self.page).to_have_url(self.url)

    def get_item_names(self):
        return self.item_names.all_text_contents()
