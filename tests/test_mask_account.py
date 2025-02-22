############################################################################
import pytest

from src.masks import get_mask_account


@pytest.mark.parametrize('value, expected', [
    (64686473678894779589, '**9589'),
    (646864736788947795899, "Введите 20-ти значное число"),
    (6468647367889477958, "Введите 20-ти значное число"),
])


def test_get_mask_account_if_int_input(value: int, expected: str) -> None:
    assert get_mask_account(value) == expected


@pytest.mark.parametrize('value, expected', [
    ('646864736788947795899', "Введите 20-ти значное число"),
    ('', "Введите 20-ти значное число"),
    (0, "Введите 20-ти значное число"),
])


def test_get_mask_account_if_str_input(value: int, expected: str) -> None:
    assert get_mask_account(value) == expected

############################################################################
