############################################################################################
from unittest.mock import patch

from src.external_api import returns_the_transaction_amount

transaction = {
    "id": 41428829,
    "state": "EXECUTED",
    "date": "2019-07-03T18:35:29.512364",
    "operationAmount": {"amount": "8221.37", "currency": {"name": "USD", "code": "USD"}},
    "description": "Перевод организации",
    "from": "MasterCard 7158300734726758",
    "to": "Счет 35383033474447895560",
}


@patch("requests.get")
def test_api_return_amount(mock_get) -> None:
    expected = {
        "success": True,
        "query": {"from": "USD", "to": "RUB", "amount": 8221.37},
        "info": {"timestamp": 1742322244, "rate": 81.751879},
        "date": "2025-03-18",
        "result": 672112.445454,
    }
    mock_get.return_value.json.return_value = expected
    assert returns_the_transaction_amount(transaction) == expected["result"]
    mock_get.assert_called_once()


############################################################################################
