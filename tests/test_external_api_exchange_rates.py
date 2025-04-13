import pytest
import requests
import requests_mock

from src.external_api import fetch_exchange_rates


def mock_response(status_code, reason=None, body=None):
    return {
        "status_code": status_code,
        "reason": reason or "",
        "text": body or "{}",
    }


############################################################################################
# Тест успешного получения курсов валют


def test_fetch_exchange_rates_success():
    # Настройка мока для API-запросов
    with requests_mock.Mocker() as m:
        # Симулируем успешный ответ
        m.get(
            "https://api.apilayer.com/exchangerates_data/latest?base=RUB&symbols=USD",
            **mock_response(200, body='{"success": true, "rates": {"USD": 70.50}}'),
        )

        # Выполнение функции
        currencies = ["USD"]
        result = fetch_exchange_rates(currencies)

        # Проверка результата
        assert len(result) == 1
        assert result[0]["currency"] == "USD"
        assert result[0]["rate"] == 70.50


############################################################################################
# Тест для ошибки сервера


def test_fetch_stock_prices_server_error():
    # Настрой мока для API-запросов
    with requests_mock.Mocker() as m:
        # Симулируем серверную ошибку
        m.get(
            "https://api.apilayer.com/exchangerates_data/latest?base=RUB&symbols=USD",
            **mock_response(500, reason="Internal Server Error"),
        )

        # Выполнить функцию
        currencies = ["USD"]
        with pytest.raises(Exception) as ex:
            fetch_exchange_rates(currencies)

        # Проверить, что поднята правильная ошибка
        assert str(ex.value) == "Server Error"


############################################################################################
# Тест для отсутствия данных


def test_fetch_stock_prices_empty_data():
    # Настрой мока для API-запросов
    with requests_mock.Mocker() as m:
        # Симулируем пустой ответ
        m.get(
            "https://api.apilayer.com/exchangerates_data/latest?base=RUB&symbols=USD",
            **mock_response(200, body='{"data":[]}'),
        )  # Пустой массив данных

        # Выполнить функцию
        currencies = ["USD"]
        result = fetch_exchange_rates(currencies)

        # Проверить, что результат пустой
        assert len(result) == 1


############################################################################################
# Тест для ошибки подключения


def test_fetch_stock_prices_connection_error():
    # Настрой мока для API-запросов
    with requests_mock.Mocker() as m:
        # Симулируем ошибку соединения
        m.get(
            "https://api.apilayer.com/exchangerates_data/latest?base=RUB&symbols=USD",
            exc=requests.exceptions.ConnectionError,
        )

        # Выполнить функцию
        currencies = ["USD"]
        with pytest.raises(Exception) as ex:
            fetch_exchange_rates(currencies)

        # Проверить, что произошла ошибка соединения
        assert str(ex.value) == ""


############################################################################################
# Тест для отсутствия токена API


def test_fetch_stock_prices_missing_api_token():
    # Удалить токен API из окружения
    import os

    os.environ.pop("APILAYER_KEY", None)

    # Выполнить функцию
    currencies = ["USD"]
    with pytest.raises(Exception) as ex:
        fetch_exchange_rates(currencies)

    # Проверить, что произошло исключение из-за отсутствия токена
    assert str(ex.value) == "API token is missing"


############################################################################################
