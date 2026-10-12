import pytest

from playwright.sync_api import expect
from models.api.post import PostResponse, PostCreate
from api.posts_api import PostsApi

@pytest.mark.smoke
@pytest.mark.api
def test_get_post(
        posts_api: PostsApi,
):
    response = posts_api.get_post(1)

    expect(response).to_be_ok()

    body = response.json()

    assert body["id"]  == 1
    assert body["userId"]  == 1
    assert body["title"]
    assert body["body"]

@pytest.mark.api
@pytest.mark.regression
def test_create_post(
        posts_api: PostsApi,
):
    payload = PostCreate(
        title="QA automation",
        body="Created by Playwright APIRequestContext",
        userId=1,
    )

    response = posts_api.create_post(payload)

    assert response.status == 201

    post = PostResponse.model_validate(
        response.json(),
    )

    assert post.title == payload.title
    assert post.body == payload.body
    assert post.user_id == payload.user_id


# def test_get_current_user(
#         authenticated_api_context: APIRequestContext,
# ):
#     response = authenticated_api_context.get("/profile")
#
#     assert response.status == 200

