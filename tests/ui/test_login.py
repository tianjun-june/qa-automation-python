import pytest
from playwright.sync_api import expect


@pytest.mark.smoke
@pytest.mark.regression
def test_successful_login(login_page, inventory_page):

    login_page.open()
    login_page.login("standard_user", "secret_sauce")


    inventory_page.verify_loaded()

@pytest.mark.regression
def test_invalid_login(login_page):

    login_page.open()
    login_page.login("invalid_user", "wrong_password")



    expect(login_page.error_message).to_be_visible()
    expect(login_page.error_message).to_contain_text(
        "Username and password do not match"
    )


def test_empty_username(login_page):

    login_page.open()
    login_page.login("", "secret_sauce")

    expect(login_page.error_message).to_be_visible()
    expect(login_page.error_message).to_contain_text(
        "Username is required"
    )

def test_inventory_has_products(login_page, inventory_page):
    login_page.open()
    login_page.login("standard_user", "secret_sauce")
    inventory_page.verify_loaded()

    product_names = inventory_page.get_product_names()

    assert len(product_names) > 0

