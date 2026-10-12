from playwright.sync_api import APIRequestContext, APIResponse

from models.api.post import PostCreate


class PostsApi:
    def __init__(self, context: APIRequestContext):
        self.context = context

    def get_post(self, post_id: int) -> APIResponse:
        return  self.context.get(f"/posts/{post_id}")

    def create_post(self, payload: PostCreate) -> APIResponse:
        return self.context.post(
            "/posts",
            data=payload.model_dump(by_alias=True),
        )

    def delete_post(self, post_id: int) -> APIResponse:
        return self.context.delete(f"/posts/{post_id}")