import pytest

from src.masks import get_mask_account


@pytest.mark.parametrize('value, expected', [
    ('64686473678894779589', '***9589'),
    ("64686473678894779589 ",),
    ("6468647367889477958",),
    (),
])

def get_mask_account(value: str, expected: str) -> None:
    assert get_mask_account(value) == expected