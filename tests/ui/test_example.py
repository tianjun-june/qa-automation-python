from playwright.sync_api import expect

def test_example_page(page):
    page.goto("https://example.com")

    # expect(
    #     page.get_by_text("THIS DOES NOT EXIST")
    # ).to_be_visible()

    assert page.title() == "Example Domain"
    assert page.get_by_role(
        "heading",
        name="Example Domain"
    ).is_visible()
