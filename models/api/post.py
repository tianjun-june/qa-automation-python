from pydantic import BaseModel, ConfigDict, Field


class PostResponse(BaseModel):
    model_config = ConfigDict(extra="forbid")

    user_id: int = Field(alias="userId")
    id: int
    title: str
    body: str


class PostCreate(BaseModel):
    model_config = ConfigDict(populate_by_name=True)
    user_id: int = Field(alias="userId")
    title: str
    body: str

