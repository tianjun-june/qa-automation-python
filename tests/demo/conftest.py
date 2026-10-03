import pytest

@pytest.fixture
def numbers():
    print("\nSETUP: prepare test data")

    a = 10
    b = 5

    yield a, b

    print("\nTEARDOWN: clean up test data")

@pytest.fixture
def calculation_data(numbers):
    a, b = numbers

    return {
        "a": a,
        "b": b,
        "expected_sum": 15,
        "expected_difference": 5,
    }

@pytest.fixture
def multiplication_data(numbers):
    a, b = numbers

    return {
        "a": a,
        "b": b,
        "expected_multiply": 50
    }


