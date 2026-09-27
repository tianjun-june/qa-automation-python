import pytest
import logging
from playwright.sync_api import expect

logger = logging.getLogger(__name__)

@pytest.mark.regression
@pytest.mark.parametrize(
    "product_name",
    [
        "Sauce Labs Backpack",
        "Sauce Labs Bike Light",
        "Sauce Labs Bolt T-Shirt",
    ],
    ids=[
        "backpack",
        "bike_light",
        "t_shirt",
    ]
)
def test_product_is_added_to_cart(
        login_page,
        inventory_page,
        cart_page,
        product_name
):
    logger.info("Testing product added to cart: %s", product_name)
    login_page.open()
    login_page.login("standard_user", "secret_sauce")

    inventory_page.add_product_to_cart(product_name)
    inventory_page.open_cart()

    cart_page.verify_loaded()

    item_names = cart_page.get_item_names()

    assert product_name in item_names

def test_add_multiple_product_to_cart(
        logged_in_inventory_page,
        cart_page,
):
    logger.info("Testing add multiple product to cart")
    products = [
        "Sauce Labs Backpack",
        "Sauce Labs Bike Light",
    ]

    for product_name in products:
        logged_in_inventory_page.add_product_to_cart(product_name)

    expect(logged_in_inventory_page.cart_badge).to_have_text("99")

    logged_in_inventory_page.open_cart()
    cart_page.verify_loaded()

    item_names = cart_page.get_item_names()

    for product_name in products:
        assert product_name in item_names
