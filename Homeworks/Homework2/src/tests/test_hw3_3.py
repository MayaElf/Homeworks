import inspect
import string

import pytest

from Homeworks.Homework2.src.main.hw3_3 import custom_range


@pytest.mark.parametrize(
    "given, expected",
    [
        ([string.ascii_lowercase, "g"], ["a", "b", "c", "d", "e", "f"]),
        (
            [string.ascii_lowercase, "g", "p"],
            ["g", "h", "i", "j", "k", "l", "m", "n", "o"],
        ),
        ([string.ascii_lowercase, "p", "g", -2], ["p", "n", "l", "j", "h"]),
        ([["a", "b", "c", "d", "e", "f", "g"], "d"], ["a", "b", "c"]),
        ([("a", "b", "c", "d", "e", "f", "g"), "d"], ["a", "b", "c"]),
    ],
)
def test_custom_range(given, expected):
    assert custom_range(*given) == expected


def test_positional_only():
    for _, kw in inspect.signature(custom_range).parameters.items():
        assert kw.default == inspect.Parameter.empty


