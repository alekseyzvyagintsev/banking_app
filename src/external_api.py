#############################################################################################
import os
from typing import Any

import requests
from dotenv import load_dotenv

from src.utils import converting_data_from_json_to_a_dict_list

load_dotenv()


def returns_the_transaction_amount(transaction: Any) -> Any:
    """
    Реализуйте функцию, которая принимает на вход транзакцию и возвращает сумму транзакции (amount) в рублях,
    тип данных — float. Если транзакция была в USD или EUR, происходит обращение к внешнему API
    для получения текущего курса валют и конвертации суммы операции в рубли.
    Для конвертации валюты воспользуйтесь Exchange Rates Data API: https://apilayer.com/exchangerates_data-api.
    """
    operation_amount = transaction.get("operationAmount")
    amount = operation_amount["amount"]
    currency = operation_amount.get("currency")
    currency_code = currency.get("code")
    if transaction:
        if operation_amount:
            if currency_code == "RUB":
                return amount
            else:
                url = "https://api.apilayer.com/exchangerates_data/convert"
                token = {"apikey": os.getenv("APILAYER_KEY")}
                # token = {"apikey": "2JDgBB9f8ff2txYJySaFPr8dFNMHvfgE"}
                params = {
                    "amount": amount,
                    "from": currency.get("code"),
                    "to": "RUB",
                }
                response = requests.get(url, headers=token, params=params)
                result = response.json()
                return result.get("result")
        else:
            print("Ключ 'operationAmount' отсутствует")
            return ""
    else:
        print("На обработку поступил пустой обьект")
        return ""


if __name__ == "__main__":
    file_with_operations = os.path.join(os.path.dirname(os.path.dirname(__file__)), "data", "operations.json")
    operations_list = converting_data_from_json_to_a_dict_list(file_with_operations)
    get_amount: Any = returns_the_transaction_amount(operations_list[1])
    print(get_amount)

############################################################################################
