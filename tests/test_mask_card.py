import pytest

from src.masks import get_mask_card_number


@pytest.mark.parametrize('value, expected', [
    ('1596837868705199', '1596 83** **** 5199'),
    ("5999414228426353 ",),
    ("599941422842635",),
    (),
])

def get_mask_card_number(value: int, expected: str) -> None:
    assert get_mask_card_number(value) == expected