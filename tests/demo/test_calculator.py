import pytest

from utils.calculator import add, subtract, multiply, divide

@pytest.mark.parametrize(
    "a,b,expected",
    [
        (1, 2, 3),
        (0, 0, 0),
        (-1, 1, 0),
        (100, 200, 300),
    ],
    ids=[
        "positive_numbers",
        "zeros",
        "negative_and_positive",
        "large_numbers",

    ]
)
def test_add(a,b,expected):
    assert add(a, b) == expected

@pytest.mark.parametrize(
    "a,b,expected",
    [
        (3, 2, 1),
        (1, 2, -1),
        (3000, 1000, 2000),
        (1000, 1000, 0),
    ],
    ids=[
        "positive_numbers",
        "negative_and_positive",
        "large_numbers",
        "zeros",
    ]
)
def test_subtract(a,b,expected):
    assert subtract(a,b) == expected

@pytest.mark.parametrize(
    "a,b,expected",
    [
        (3, 2, 6),
        (0, 2, 0),
        (-2, 3, -6),
        (100, 1000, 100000),
    ],
    ids=[
        "positive_numbers",
        "zeros",
        "negative_and_positive",
        "large_numbers",
    ]
)
def test_multiply(a,b,expected):
    assert multiply(a, b) == expected


@pytest.mark.parametrize(
    "a,b,expected",
    [
        (10, 2, 5),
        (0, 3, 0),
        (-10, 2, -5),
        (1, 2, 0.5),
        (1000,2,500)
    ],
    ids=[
        "positive_numbers",
        "zeros",
        "negative_and_positive",
        "Decimal",
        "large_numbers",
    ]
)
def test_divide(a,b,expected):
    assert divide(a, b) == expected

def test_add_with_fixtures(numbers):
    a, b = numbers
    assert add(a, b) == 15

def test_divide_by_zero():
    with pytest.raises(ZeroDivisionError):
        divide(10,0)

def test_subtract_with_fixtures(numbers):
    a, b = numbers
    assert subtract(a, b) == 5

def test_calculation_data(calculation_data):
    assert add(
        calculation_data["a"],
        calculation_data["b"]
    ) == calculation_data["expected_sum"]

def test_multiply_with_fixture(multiplication_data):
    assert multiply(
        multiplication_data["a"],
        multiplication_data["b"]
    ) == multiplication_data["expected_multiply"]

