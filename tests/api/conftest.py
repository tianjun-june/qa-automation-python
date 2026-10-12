from collections.abc import Iterable
from typing import Iterator

import pytest

from playwright.sync_api import Playwright, APIRequestContext

from models.api.auth import LoginResponse
from utils.config_loader import AppConfig
from api.posts_api import PostsApi


@pytest.fixture(scope="session")
def api_context(
        playwright: Playwright,
        app_config: AppConfig,
) -> Iterable[APIRequestContext]:
    context = playwright.request.new_context(
        base_url=app_config.api_base_url,
    )

    yield context

    context.dispose()

@pytest.fixture(scope="session")
def auth_token(
        api_context: APIRequestContext,
        app_config: AppConfig,
) -> str:
    response = api_context.post(
        "/auth/login",

    data={
        "username": app_config.credentials.username,
        "password": app_config.credentials.password,
    },
    )

    assert response.status == 200

    login_response = LoginResponse.model_validate(
        response.json(),
    )

    return login_response.access_token

@pytest.fixture(scope="session")
def authenticated_api_context(
        playwright: Playwright,
        app_config: AppConfig,
        auth_token: str,
) -> Iterator[APIRequestContext]:

    context = playwright.request.new_context(
        base_url=app_config.api_base_url,
        extra_http_headers={"Authorization": f"Bearer {auth_token}"},
    )

    yield context
    context.dispose()

@pytest.fixture
def posts_api(
        api_context: APIRequestContext,
) -> PostsApi:
    return PostsApi(api_context)



