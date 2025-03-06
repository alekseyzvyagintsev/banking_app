##################################################################################################
import pytest

from typing import Any #, Iterable #, Optional

from src.generators import filter_by_currency

@pytest.mark.parametrize(
    "code, expected",
    [
        ("USD",
            [{
                "id": 939719570,
                "state": "EXECUTED",
                "date": "2018-06-30T02:08:58.425572",
                "operationAmount": {
                    "amount": "9824.07",
                    "currency": {
                        "name": "USD",
                        "code": "USD"
                }
                },
                "description": "Перевод организации",
                "from": "Счет 75106830613657916952",
                "to": "Счет 11776614605963066702"
            },
            {
                "id": 142264268,
                "state": "EXECUTED",
                "date": "2019-04-04T23:20:05.206878",
                "operationAmount": {
                    "amount": "79114.93",
                    "currency": {
                        "name": "USD",
                        "code": "USD"
                    }
                },
                "description": "Перевод со счета на счет",
                "from": "Счет 19708645243227258542",
                "to": "Счет 75651667383060284188"
            }]
        )
    ],
)

def test_filter_by_usd(transactions_data, code: str, expected: list[dict[str, Any]]) -> None:
    """Тест generators.filter_by_currency фильтрации списка по типу валюты USD"""
    usd_out = []
    usd_transactions = filter_by_currency(transactions_data, code)
    for _ in range(2):
        usd_out.append(next(iter(usd_transactions)))
    print(usd_out)
    assert usd_out == expected


@pytest.mark.parametrize(
    "code, expected",
    [
        ("RUB",
            [{
            "id": 873106923,
            "state": "EXECUTED",
            "date": "2019-03-23T01:09:46.296404",
            "operationAmount": {
                "amount": "43318.34",
                "currency": {
                    "name": "руб.",
                    "code": "RUB"
                }
            },
            "description": "Перевод со счета на счет",
            "from": "Счет 44812258784861134719",
            "to": "Счет 74489636417521191160"
        },
        {
            "id": 594226727,
            "state": "CANCELED",
            "date": "2018-09-12T21:27:25.241689",
            "operationAmount": {
                "amount": "67314.70",
                "currency": {
                    "name": "руб.",
                    "code": "RUB"
                }
            },
            "description": "Перевод организации",
            "from": "Visa Platinum 1246377376343588",
            "to": "Счет 14211924144426031657"
        }]
        )
    ],
)

def test_filter_by_rub(transactions_data, code: str, expected: list[dict[str, Any]]) -> None:
    """Тест generators.filter_by_currency фильтрации списка по типу валюты RUB"""
    transactions = transactions_data
    rub_out = []
    rub_transactions = filter_by_currency(transactions, code)
    for _ in range(2):
        rub_out.append(next(iter(rub_transactions)))
    print(rub_out)
    assert rub_out == expected


def test_by_empty_list_filter_by_rub() -> None:
    """Тест generators.filter_by_currency фильтрации пустого списка по типу валюты RUB"""
    rub_out = []
    rub_transactions = filter_by_currency([], "RUB")
    for _ in range(2):
        rub_out.append(next(iter(rub_transactions)))
    print(rub_out)
    assert rub_out == ['С', 'С']


def test__by_empty_list_filter_currency() -> None:
    """Тест generators.filter_by_currency фильтрации пустого списка без передачи типа валюты"""
    currency_transactions = (filter_by_currency([]))
    print(currency_transactions)
    assert currency_transactions == "Список пуст"

##################################################################################################
