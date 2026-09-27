def test_example_locator(page):
    page.goto("https://example.com")

    heading = page.get_by_role("heading", name="Example Domain")
    link = page.get_by_role("link", name="Learn more")

    assert heading.is_visible()
    assert link.is_visible()

def test_learn_more_link(page):
    page.goto("https://example.com")

    link = page.get_by_role("link", name="Learn more")

    link.click()

    assert "iana.org" in page.url