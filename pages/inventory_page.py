import re
import logging
from playwright.sync_api import Page, expect


logger = logging.getLogger(__name__)

class InventoryPage:

    # URL = f"{BASE_URL}/inventory.html"

    def __init__(self, page: Page):
        self.page = page

        self.title = page.get_by_text("Products")
        self.product_items = page.locator(".inventory_item")
        self.cart_badge = page.locator(".shopping_cart_badge")
        self.cart_link = page.locator(".shopping_cart_link")
        self.menu_button = page.get_by_role("button", name="Open Menu")
        self.menu_about_button = page.get_by_role("link", name="About")
        self.x_icon = page.get_by_role("link",name="x")

    def open(self):
        self.page.goto("/inventory.html")

    def verify_loaded(self):
        logger.info("Verifying inventory page is loaded")

        expect(self.page).to_have_url(re.compile(r".*/inventory\.html$"))
        expect(self.title).to_be_visible()

    def get_product_names(self):

        return self.page.locator(".inventory_item_name").all_text_contents()

    def add_product_to_cart(self, product_name:str):
        logger.info("Adding product to cart: %s", product_name)

        product = self.product_items.filter(
            has_text=product_name
        )

        product.get_by_role(
            "button",
            name="Add to cart",
        ).click()

    def open_cart(self):
        logger.info("Opening shopping cart")
        self.cart_link.click()

    def open_menu(self):
        logger.info("Opening menu")
        self.menu_button.click()

    def open_about(self):
        logger.info("Opening new tab...")
        self.menu_about_button.click()

    def open_x_saucelab(self):
        logger.info("Opening X_saucelab")
        self.x_icon.click()