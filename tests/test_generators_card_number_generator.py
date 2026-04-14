##################################################################################################
import pytest

from src.generators import card_number_generator


def test_card_number_generator() -> None:
    """Тест генератора номеров кредитных карт с параметрами star=1, stop=5"""
    answers = [
        "0000 0000 0000 0001",
        "0000 0000 0000 0002",
        "0000 0000 0000 0003",
        "0000 0000 0000 0004",
        "0000 0000 0000 0005",
    ]

    card_numbers = card_number_generator(1, 5)
    for answer in answers:
        card_number = next(card_numbers)
        assert card_number == answer


def test_card_number_generator_end_list() -> None:
    """Тест генератора номеров кредитных карт с параметрами
    star=9999999999999989, stop=9999999999999999"""

    answers = [
        "9999 9999 9999 9989",
        "9999 9999 9999 9990",
        "9999 9999 9999 9991",
        "9999 9999 9999 9992",
        "9999 9999 9999 9993",
        "9999 9999 9999 9994",
        "9999 9999 9999 9995",
        "9999 9999 9999 9996",
        "9999 9999 9999 9997",
        "9999 9999 9999 9998",
        "9999 9999 9999 9999",
    ]

    card_numbers = card_number_generator(9999999999999989, 9999999999999999)
    for answer in answers:
        card_number = next(card_numbers)
        assert card_number == answer


def test_card_number_generator_negative_start() -> None:
    """Тест генератора номеров кредитных карт с параметрами star=-3, stop=5"""

    answers = [
        "0000 0000 0000 0001",
        "0000 0000 0000 0002",
        "0000 0000 0000 0003",
        "0000 0000 0000 0004",
        "0000 0000 0000 0005",
    ]

    card_numbers = card_number_generator(-3, 5)
    for answer in answers:
        card_number = next(card_numbers)
        assert card_number == answer


def test_card_number_generator_start_after_stop() -> None:
    """Тест генератора номеров кредитных карт с параметрами star=6, stop=1"""

    with pytest.raises(ValueError):
        card_number_generator(6, 1)
        raise ValueError("Something went wrong")


##################################################################################################
