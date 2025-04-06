#############################################################################################
import os
import yfinance as yf

from dataclasses import dataclass
from typing import Any, List

import requests
from dotenv import load_dotenv

from src.logging_external_api import logger
from src.utils import read_user_settings

load_dotenv()


def returns_the_transaction_amount(transaction: Any) -> Any:
    """
    Функция принимает на вход транзакцию и возвращает сумму транзакции (amount) в рублях,
    тип данных — float. Если транзакция была в USD или EUR, происходит обращение к внешнему API
    для получения текущего курса валют и конвертации суммы операции в рубли.
    Для конвертации валюты воспользуйтесь Exchange Rates Data API: https://apilayer.com/exchangerates_data-api.
    """
    operation_amount = transaction.get("operationAmount")
    amount = operation_amount["amount"]
    currency = operation_amount.get("currency")
    currency_code = currency.get("code")
    if transaction:
        logger.info("Проверяем если транзакция рублевая, возвращаем как есть")
        if operation_amount:
            if currency_code == "RUB":
                return amount
            else:
                logger.info("Транзакция не в рублях, поэтому обращаемся к внешнему API за обменным курсом")
                url = "https://api.apilayer.com/exchangerates_data/convert"
                token = {"apikey": os.getenv("APILAYER_KEY")}
                # token = {"apikey": "2JDgBB9f8ff2txYJySaFPr8dFNMHvfgE"}
                params = {
                    "amount": amount,
                    "from": currency.get("code"),
                    "to": "RUB",
                }
                logger.info("Получаем ответ от сервера")
                response = requests.get(url, headers=token, params=params)
                if response.status_code == 200:
                    result = response.json()
                    logger.info(f"Положительный ответ получен: {result}")
                    return result.get("result")
                elif response.status_code == 500:
                    logger.error(Exception("Server Error"))
                    raise Exception("Server Error")
                else:
                    logger.error(f"Site error: {response.reason}")
        else:
            logger.error("Ключ 'operationAmount' отсутствует")
            return ""
    else:
        print("На обработку поступил пустой объект")
        return ""


# if __name__ == "__main__":
#     file_with_operations = os.path.join(os.path.dirname(os.path.dirname(__file__)), "data", "operations.json")
#     operations_list = get_json_data(file_with_operations)
#     get_amount: Any = returns_the_transaction_amount(operations_list[1])
#     print(operations_list[1])
#     print(get_amount)

############################################################################################
class CurrencyRate:
    def __init__(self, currency: str, rate: float):
        self.currency = currency
        self.rate = rate


def fetch_exchange_rates(currencies: list[str]) -> list[CurrencyRate]: #[CurrencyRate]:
    rates = []
    for currency in currencies:
        logger.info("Получаем ответ от сервера")
        url = 'https://api.apilayer.com/exchangerates_data/latest'
        token = {"apikey": os.getenv("APILAYER_KEY")}
        payload = {}
        params = {
            'base': 'RUB',
            'symbols': currency
        }
        response = requests.get(url, headers=token, params=params, data=payload)
        if response.status_code == 200:
            rate = response.json()["rates"]
            rates.append(CurrencyRate(currency, rate))
        elif response.status_code == 500:
            logger.error(Exception("Server Error"))
            raise Exception("Server Error")
        else:
            logger.error(f"Site error: {response.reason}")
    return rates

# if __name__ == '__main__':
#     user_settings = read_user_settings(
#         os.path.join(os.path.dirname(os.path.dirname(__file__)),
#                      "data/user_settings.json")
#     )
#     currencies = user_settings.get("user_currencies")
#     exchange_rates = fetch_exchange_rates(currencies)


############################################################################################
class StockPrice:
    def __init__(self, stock: str, price: float):
        self.stock = stock
        self.price = price


def fetch_stock_prices(stocks: list) -> list[StockPrice]:

    prices = []

    # Получение цен всех акций
    tickers_data = yf.Tickers(' '.join(stocks)).tickers

    for ticker in stocks:
        try:
            # Получение текущей цены акции
            price = tickers_data[ticker].info['regularMarketPrice']
            prices.append(StockPrice(ticker, price))
        except KeyError:
            print(f"Не удалось получить цену для {ticker}.")

    return prices


# if __name__ == '__main__':
#     user_settings = read_user_settings(
#         os.path.join(os.path.dirname(os.path.dirname(__file__)),
#                      "data/user_settings.json")
#     )
#     stocks = user_settings.get("user_stocks")
#     exchange_rates = fetch_stock_prices(stocks)
#     print(exchange_rates)
############################################################################################
