import pytest

from src.widget import get_date


@pytest.mark.parametrize('value, expected', [
    ("2024-03-11T02:26:18.671407", "11.03.2024"),
    ("2024-03-1102:26:18.671407",),
    (["2024-03-11T02:26:18.67140"],),
    ("T02:26:18.671407",),
    (),
])

def get_date(value: str, expected: str) -> None:
    assert get_date(value) == expected
