import pytest
import logging
from playwright.sync_api import expect
from test_data.suacedemo import Products

logger = logging.getLogger(__name__)

@pytest.mark.regression
@pytest.mark.parametrize(
    "product_name",
    [
        Products.BACKPACK,
        Products.BIKE_LIGHT,
        Products.BOLT_T_SHIRT
    ],
)
def test_product_is_added_to_cart(
        logged_in_inventory_page,
        cart_page,
        product_name
):
    logger.info("Testing product added to cart: %s", product_name)

    logged_in_inventory_page.add_product_to_cart(product_name)
    logged_in_inventory_page.open_cart()

    cart_page.verify_loaded()

    item_names = cart_page.get_item_names()

    assert product_name in item_names

def test_add_multiple_product_to_cart(
        logged_in_inventory_page,
        cart_page,
):
    logger.info("Testing add multiple product to cart")
    products = [
        Products.BACKPACK,
        Products.BIKE_LIGHT,
    ]

    for product_name in products:
        logged_in_inventory_page.add_product_to_cart(product_name)

    expect(logged_in_inventory_page.cart_badge).to_have_text("2")

    logged_in_inventory_page.open_cart()
    cart_page.verify_loaded()

    item_names = cart_page.get_item_names()

    for product_name in products:
        assert product_name in item_names
