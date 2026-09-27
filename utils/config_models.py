from pydantic import BaseModel, ConfigDict


class BrowserConfig(BaseModel):
    model_config = ConfigDict(
        extra="forbid",
        strict=True,
    )

    timeout: int
    headless: bool


class TestConfig(BaseModel):
    model_config = ConfigDict(
        extra="forbid",
        strict=True,
    )

    screenshot_on_failure: bool
    retries: int

class CredentialsConfig(BaseModel):
    model_config = ConfigDict(
        extra="forbid",
        strict=True,
    )

    username: str
    password: str

class AppConfig(BaseModel):
    model_config = ConfigDict(
        extra="forbid",
        strict=True,
    )

    base_url: str
    browser: BrowserConfig
    test: TestConfig
    credentials: CredentialsConfig