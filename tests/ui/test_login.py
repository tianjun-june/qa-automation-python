import pytest
from playwright.sync_api import expect

from test_data.suacedemo import INVALID_LOGIN_CASES


@pytest.mark.smoke
@pytest.mark.regression
def test_successful_login(login_page, inventory_page):

    login_page.open()
    login_page.login("standard_user", "secret_sauce")


    inventory_page.verify_loaded()
    # expect(inventory_page.cart_badge).to_have_text("1")

@pytest.mark.regression
@pytest.mark.parametrize(
    "case",
    INVALID_LOGIN_CASES,
    ids=lambda case: case.id,
)
def test_invalid_login(login_page, case):

    login_page.open()
    login_page.login(case.username, case.password)

    login_page.verify_loaded(case.expected_message)

def test_inventory_has_products(login_page, inventory_page):
    login_page.open()
    login_page.login("standard_user", "secret_sauce")
    inventory_page.verify_loaded()

    product_names = inventory_page.get_product_names()

    assert len(product_names) > 0

