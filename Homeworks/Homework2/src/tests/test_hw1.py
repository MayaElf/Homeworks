import pytest

from Homeworks.Homework2.src.main.hw1 import major_and_minor_elem

LISTS = [
    ([2, 2, 1, 1, 1, 2, 2], (2, 1)), 
    ([3, 2, 3], (3, 2)),
    ([3, 3, 2, 2, 3, 3, 1], (3, 1))
]


@pytest.mark.parametrize(
    "numbers, expected", LISTS
)
def test_major_and_minor_elem(numbers, expected):
    assert major_and_minor_elem(numbers) == expected
