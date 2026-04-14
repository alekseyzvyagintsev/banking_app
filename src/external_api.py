#############################################################################################
import os
from typing import Any

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


############################################################################################
def fetch_exchange_rates(currencies: list[str]) -> list[dict]:  # [CurrencyRate]:
    """Функция для получения курса валют из входящего списка валют."""
    rates = []
    if not currencies:
        return rates
    if not os.getenv("APILAYER_KEY"):
        raise ValueError("API token is missing")
    for currency in currencies:
        logger.info("Получаем ответ от сервера")
        url = "https://api.apilayer.com/exchangerates_data/latest"
        token = {"apikey": os.getenv("APILAYER_KEY")}
        params = {"base": "RUB", "symbols": currency}
        response = requests.get(url, headers=token, params=params)
        if response.status_code == 200:
            logger.info("От сервера получен положительный ответ")
            rate = response.json().get("rates", {}).get(currency)
            rates.append({"currency": currency, "rate": rate})
        elif response.status_code == 500:
            logger.error(Exception("Server Error"))
            raise Exception("Server Error")
        else:
            logger.error(f"Возникла ошибка: {response.reason}")
            raise Exception(f"Возникла ошибка: {response.reason}")
    return rates


############################################################################################
def fetch_stock_prices(stocks: list) -> list[dict]:
    """Функция для получения курса акций из входящего списка акций."""
    prices = []
    if not os.getenv("STOCKDATA_API_KEY"):
        raise ValueError("API token is missing")
    if not stocks:
        return stocks
    for stock in stocks:
        try:
            logger.info("Получаем ответ от сервера")
            response = requests.get(
                f"https://api.stockdata.org/v1/data/quote?symbols={stock}&api_token={os.getenv('STOCKDATA_API_KEY')}"
            )
            if response.status_code == 200:
                logger.info("От сервера получен положительный ответ")
                data = response.json().get("data", [])
                for item in data:
                    prices.append({"stock": item["ticker"], "price": item["price"]})
            elif response.status_code == 500:
                logger.error(Exception("Server Error"))
                raise Exception("Server Error")
        except Exception as ex:
            logger.error(f"Произошла ошибка: {ex}")
            raise Exception(f"Произошла ошибка: {ex}")

    return prices


############################################################################################
