import pytest
from playwright.sync_api import expect
from test_data.suacedemo import Products

@pytest.mark.smoke
def test_add_product_to_cart(logged_in_inventory_page):

    logged_in_inventory_page.add_product_to_cart(Products.BACKPACK)

    expect(
        logged_in_inventory_page.cart_badge
    ).to_have_text("1")

def test_inventory_has_products(logged_in_inventory_page):


    product_names = logged_in_inventory_page.get_product_names()
    assert len(product_names) > 0

    print(product_names)