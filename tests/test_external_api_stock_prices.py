import os

import pytest
import requests
import requests_mock

from src.external_api import fetch_stock_prices


# Определение функции для создания моков ответов
def mock_response(status_code, reason=None, body=None):
    return {
        "status_code": status_code,
        "reason": reason or "",
        "text": body or "{}",
    }


############################################################################################
# Тест для успешного сценария


def test_fetch_stock_prices_success():
    # Настрой мока для API-запросов
    with requests_mock.Mocker() as m:
        # Симулируем успешный ответ
        m.get(
            "https://api.stockdata.org/v1/data/quote?symbols=AAPL",
            **mock_response(200, body='{"data":[{"ticker":"AAPL","price":100}]}'),
        )

        # Выполнить функцию
        stocks = ["AAPL"]
        results = fetch_stock_prices(stocks)

        # Проверить результат
        assert len(results) == 1
        assert results[0]["stock"] == "AAPL"
        assert results[0]["price"] == 100


############################################################################################
# Тест для ошибки сервера


def test_fetch_stock_prices_server_error():
    # Настрой мока для API-запросов
    with requests_mock.Mocker() as m:
        # Симулируем серверную ошибку
        m.get(
            "https://api.stockdata.org/v1/data/quote?symbols=AAPL",
            **mock_response(500, reason="Internal Server Error"),
        )

        # Выполнить функцию
        stocks = ["AAPL"]
        with pytest.raises(Exception) as ex:
            fetch_stock_prices(stocks)

        # Проверить, что поднята правильная ошибка
        assert str(ex.value) == "Произошла ошибка: Server Error"


############################################################################################
# Тест для отсутствия данных


def test_fetch_stock_prices_empty_data():
    # Настрой мока для API-запросов
    with requests_mock.Mocker() as m:
        # Симулируем пустой ответ
        m.get(
            "https://api.stockdata.org/v1/data/quote?symbols=AAPL", **mock_response(200, body='{"data":[]}')
        )  # Пустой массив данных

        # Выполнить функцию
        stocks = ["AAPL"]
        results = fetch_stock_prices(stocks)

        # Проверить, что результат пустой
        assert len(results) == 0


############################################################################################
# Тест для ошибки подключения


def test_fetch_stock_prices_connection_error():
    # Настрой мока для API-запросов
    with requests_mock.Mocker() as m:
        # Симулируем ошибку соединения
        m.get("https://api.stockdata.org/v1/data/quote?symbols=AAPL", exc=requests.exceptions.ConnectionError)

        # Выполнить функцию
        stocks = ["AAPL"]
        with pytest.raises(Exception) as ex:
            fetch_stock_prices(stocks)

        # Проверить, что произошла ошибка соединения
        assert str(ex.value) == "Произошла ошибка: "


############################################################################################
# Тест для отсутствия токена API


def test_fetch_stock_prices_missing_api_token():
    # Удалить токен API из окружения
    os.environ.pop("STOCKDATA_API_KEY", None)

    # Выполнить функцию
    stocks = ["AAPL"]
    with pytest.raises(Exception) as ex:
        fetch_stock_prices(stocks)

    # Проверить, что произошло исключение из-за отсутствия токена
    assert str(ex.value) == "API token is missing"


############################################################################################
