from dataclasses import dataclass

@dataclass(frozen=True)
class LoginCase:
    id: str
    username: str
    password: str
    expected_message: str


INVALID_LOGIN_CASES = [
    LoginCase(
        id="invalid_credentials",
        username="invalid_user",
        password="wrong_password",
        expected_message=(
            "Epic sadface: Username and password do not match "
            "any user in this service"
        )
    ),
    LoginCase(
        id="missing_password",
        username="invalid_user",
        password="",
        expected_message="Epic sadface: Password is required",
    ),
    LoginCase(
        id="invalid_username",
        username="",
        password="wrong_password",
        expected_message="Epic sadface: Username is required",
    )
]


class Products:
    BACKPACK = "Sauce Labs Backpack"
    BIKE_LIGHT = "Sauce Labs Bike Light"
    BOLT_T_SHIRT = "Sauce Labs Bolt T-Shirt"



