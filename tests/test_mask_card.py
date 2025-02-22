############################################################################
import pytest

from src.masks import get_mask_card_number


@pytest.mark.parametrize('value, expected', [
    (1596837868705199, '1596 83** **** 5199'),
    (646864736788947795899, "Введите 16-ти значное число"),
    (6468647367889477958, "Введите 16-ти значное число"),
])
def test_get_mask_card_number_if_int_input(value: int, expected: str) -> None:
    assert get_mask_card_number(value) == expected


@pytest.mark.parametrize('value, expected', [
    ('646864736788947795899', "Введите 16-ти значное число"),
    ('', "Введите 16-ти значное число"),
    (0, "Введите 16-ти значное число"),
])
def test_get_mask_card_number_if_str_input(value: int, expected: str) -> None:
    assert get_mask_card_number(value) == expected

############################################################################
