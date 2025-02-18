import pytest

from src.widget import mask_account_card


@pytest.mark.parametrize('value, expected', [
    ('Maestro 1596837868705199', 'Maestro 1596 83** **** 5199'),
    ("Visa Classic 6831982476737658", "Visa Classic 6831 98** **** 7658"),
    ("Visa Gold 5999414228426353 ",),
    ("Visa Gold 599941422842635",),
    ('Счет 64686473678894779589', 'Счет ***9589'),
    ("Счет 64686473678894779589 ",),
    ("Счет 6468647367889477958",),
    (),
])

def mask_account_card(value: str, expected: str) -> None:
    assert mask_account_card(value) == expected