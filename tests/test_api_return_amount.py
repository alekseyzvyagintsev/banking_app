############################################################################################
# from unittest.mock import patch
#
# from src.external_api import returns_the_transaction_amount
#
# transaction = {
#     "id": 41428829,
#     "state": "EXECUTED",
#     "date": "2019-07-03T18:35:29.512364",
#     "operationAmount": {"amount": "8221.37", "currency": {"name": "USD", "code": "USD"}},
#     "description": "Перевод организации",
#     "from": "MasterCard 7158300734726758",
#     "to": "Счет 35383033474447895560",
# }
#
#
# @patch('src.external_api.requests')
# def test_api_return_amount(mock_requests):
#     """ Тест функции на правильность """
#     expected = {
#         "success": True,
#         "query": {"from": "USD", "to": "RUB", "amount": 8221.37},
#         "info": {"timestamp": 1742322244, "rate": 81.751879},
#         "date": "2025-03-18",
#         "result": 697478.315155,
#     }
#
#     mock_response = mock_requests.get.return_value
#     mock_response.json.return_value = expected
#
#     result = returns_the_transaction_amount(transaction)
#     mock_requests.get.assert_called_once()
#     assert result == expected["result"]

from unittest.mock import patch

import pytest

from src.external_api import returns_the_transaction_amount

# Фикстура для транзакции
transaction = {
    "id": 41428829,
    "state": "EXECUTED",
    "date": "2019-07-03T18:35:29.512364",
    "operationAmount": {"amount": "8221.37", "currency": {"name": "USD", "code": "USD"}},
    "description": "Перевод организации",
    "from": "MasterCard 7158300734726758",
    "to": "Счет 35383033474447895560",
}


# Тест успешности конверсии
@patch("src.external_api.requests")
def test_api_return_amount_success(mock_requests):
    """Тест успешного возврата результата конверсии."""
    expected = {
        "success": True,
        "query": {"from": "USD", "to": "RUB", "amount": 8221.37},
        "info": {"timestamp": 1742322244, "rate": 81.751879},
        "date": "2025-03-18",
        "result": 672112.445454,
    }

    mock_response = mock_requests.get.return_value
    mock_response.status_code = 200  # Код нормальной работы сервиса
    mock_response.json.return_value = expected

    result = returns_the_transaction_amount(transaction)
    print(result)
    mock_requests.get.assert_called_once()
    assert result == expected["result"]


# Тест отсутствия данных от API
@patch("src.external_api.requests")
def test_api_return_amount_missing_data(mock_requests):
    """Тест отсутствия данных от API."""
    mock_response = mock_requests.get.return_value
    mock_response.status_code = 200  # Код нормальной работы сервиса
    mock_response.json.return_value = {}  # Пустой ответ от API

    result = returns_the_transaction_amount(transaction)
    mock_requests.get.assert_called_once()
    assert result is None  # Ожидание отсутствия результата


# Тест ошибки сервера API
@patch("src.external_api.requests")
def test_api_return_amount_server_error(mock_requests):
    """Тест случая, когда сервер API возвращает ошибку."""
    mock_response = mock_requests.get.return_value
    mock_response.status_code = 500  # Код ошибки сервера
    mock_response.json.side_effect = Exception("Server Error")  # Искусственная ошибка сервера

    with pytest.raises(Exception) as ex:
        returns_the_transaction_amount(transaction)
    mock_requests.get.assert_called_once()
    assert str(ex.value) == "Server Error"


# Тест неверной валюты
@patch("src.external_api.requests")
def test_api_return_amount_invalid_currency(mock_requests):
    """Тест случая, когда валюта не поддерживается."""
    transaction_invalid_currency = {
        "id": 41428829,
        "state": "EXECUTED",
        "date": "2019-07-03T18:35:29.512364",
        "operationAmount": {
            "amount": "8221.37",
            "currency": {"name": "XXX", "code": "XXX"},
        },  # Неподдерживаемая валюта
        "description": "Перевод организации",
        "from": "MasterCard 7158300734726758",
        "to": "Счет 35383033474447895560",
    }

    result = returns_the_transaction_amount(transaction_invalid_currency)
    assert result is None  # Ожидание отсутствия результата при неподдерживаемой валюте


# Тест неправильного формата данных
@patch("src.external_api.requests")
def test_api_return_amount_wrong_format(mock_requests):
    """Тест случая, когда данные от API имеют неправильный формат."""
    mock_response = mock_requests.get.return_value
    mock_response.json.return_value = {"result": "invalid format"}  # Не числовой результат

    result = returns_the_transaction_amount(transaction)
    mock_requests.get.assert_called_once()
    assert result is None  # Ожидание отсутствия результата при неправильном формате данных


# Тест соединения с несуществующим API
@patch("src.external_api.requests")
def test_api_return_amount_nonexistent_api(mock_requests):
    """Тест попытки обращения к несуществующему API."""
    mock_requests.get.side_effect = ConnectionError("Connection refused")

    with pytest.raises(ConnectionError) as exc_info:
        returns_the_transaction_amount(transaction)
    assert str(exc_info.value) == "Connection refused"


############################################################################################
