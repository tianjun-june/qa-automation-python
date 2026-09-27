import pytest
from playwright.sync_api import expect

@pytest.mark.smoke
def test_add_product_to_cart(login_page, inventory_page):
    login_page.open()
    login_page.login("standard_user", "secret_sauce")

    inventory_page.verify_loaded()

    inventory_page.add_product_to_cart("Sauce Labs Backpack")

    expect(
        inventory_page.cart_badge
    ).to_have_text("1")

def test_inventory_has_products(login_page, inventory_page):
    login_page.open()
    login_page.login("standard_user", "secret_sauce")

    inventory_page.verify_loaded()

    product_names = inventory_page.get_product_names()
    assert len(product_names) > 0

    print(product_names)