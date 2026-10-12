import pytest

from playwright.sync_api import APIRequestContext, expect


@pytest.mark.api
@pytest.mark.smoke
def test_application_is_available(
        api_context: APIRequestContext,
):
    response = api_context.get("/")

    expect(response).to_be_ok()
