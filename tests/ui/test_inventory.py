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

@pytest.mark.regression
def test_inventory_loaded(authenticated_inventory_page):
    authenticated_inventory_page.open()
    authenticated_inventory_page.verify_loaded()

@pytest.mark.regression
def test_inventory_loaded2(authenticated_inventory_page):
    authenticated_inventory_page.open()
    authenticated_inventory_page.verify_loaded()

def test_open_x_saucelab(authenticated_inventory_page):

    authenticated_inventory_page.open()
    authenticated_inventory_page.verify_loaded()

    # test open new tab
    # with authenticated_inventory_page.page.expect_popup() as popup_info:
    #     authenticated_inventory_page.open_x_saucelab()
    #
    # x_saucelab_page = popup_info.value
    # expect(x_saucelab_page.get_by_role("link", name="2008")).to_be_visible()
    # x_saucelab_page.close()
    # x_saucelab_page.opener

    authenticated_inventory_page.page.bring_to_front()


