import logging
import time

from playwright.sync_api import expect
from requests import delete

logger = logging.getLogger(__name__)

def test_download_complete_order_pdf(
        authenticated_checkout_complete_page,
        authenticated_checkout_step_two_page,
        tmp_path,
):
    authenticated_checkout_step_two_page.open()

    authenticated_checkout_step_two_page.verify_checkout_step_two_is_loaded()

    authenticated_checkout_step_two_page.finish_checkout()

    authenticated_checkout_complete_page.verify_checkout_complete_is_loaded()

    with authenticated_checkout_complete_page.page.expect_download() as download_info:
        logger.info(f"Download starting...")
        authenticated_checkout_complete_page.generate_pdf_order()

    download = download_info.value
    target = tmp_path / download.suggested_filename
    logger.info(f"Download path: {target}")
    download.save_as(target)
    logger.info(f"Download complete")
    assert target.exists()

def test_alert(page):
    page.set_content(
        """
        <button onclick="alert('Order completed')">
        Show alert
        </button>"""
    )

    def handle_dialog(dialog):
        assert dialog.message == "Order completed"
        dialog.accept()

    page.once("dialog", handle_dialog)


    page.get_by_role(
        "button",
        name="Show alert",
    ).click()

    logger.info(f"Alert clicked")

def test_confirm(page):
    page.set_content("""
    <button onclick="if (confirm('Delete order?')) {
    document.querySelector('#result').textContent = 'deleted';
    } else {
    document.querySelector('#result').textContent = 'cancelled';}" >
    Delete </button>
    <div id="result"></div>
    """)

    page.once(
        "dialog",
        lambda dialog: dialog.accept(),
    )

    delete_button = page.get_by_role(
        "button",
        name="Delete",
    )

    delete_button.click()

    def handle_dialog(dialog):
        dialog.dismiss()

    delete_button.click()

    page.once("dialog", handle_dialog)

def test_prompt(page):
    page.set_content("""
    <button onclick="
        const name = prompt('Enter your name');
        document.querySelector('#result').textContent = name;
    ">  Enter name
    </button>
    
    <div id="result"></div>
    """)
    def handle_dialog(dialog):
        assert dialog.message == "Enter your name"
        dialog.accept("Tom")

    page.once("dialog", handle_dialog)

    page.get_by_role("button", name="Enter name").click()

    expect(
        page.locator("#result")
    ).to_have_text("Tom")
