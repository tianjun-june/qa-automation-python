base1 = {
        "browser": {
            "headless": True,
            "timeout": 10000
        }
    }

override1 = {
    "browser": {
        "timeout": 20000
    }
}

def merge_exercise(base, override):
    result = base.copy()

    for key, value in override.items():

        if(
            key in result
            and isinstance(result[key], dict)
            and isinstance(value, dict)
        ):
            result[key] = merge_exercise(result[key], value)
        else:
            result[key] = value

    return result
def test_recursion():
    print(merge_exercise(base1, override1))