##################################################################################################
import pytest

from typing import Any #, Iterable #, Optional

from src.generators import filter_by_currency
# from tests.conftest import transactions_data

@pytest.mark.parametrize(
    "code, expected",
    [
        ('USD',
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

def test_filter_by_currency(transactions_data, code: str, expected: list[dict[str, Any]]) -> None:
    transactions = transactions_data
    usd_out = []
    usd_transactions = filter_by_currency(transactions, code)
    for _ in range(2):
        usd_out.append(next(iter(usd_transactions)))
    print(usd_out)
    assert usd_out == expected

##################################################################################################
