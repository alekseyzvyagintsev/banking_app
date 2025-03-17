#############################################################################################
import os
import json
from typing import Any
from utils import converting_data_into_a_dict_list
import requests

from dotenv import load_dotenv

load_dotenv()

def returns_the_transaction_amount(transaction: Any) -> str | float:
    """
    функция принимает на вход транзакцию и возвращает сумму транзакции (amount) в рублях,
    тип данных — float. Если транзакция была в USD или EUR, происходит обращение к внешнему API
    для получения текущего курса валют и конвертации суммы операции в рубли.
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
                token = {"apikey": "2JDgBB9f8ff2txYJySaFPr8dFNMHvfgE"}
                params = {
                    "amount": amount,
                    "from": currency.get("code"),
                    "to": "RUB",
                }

                response = requests.request("GET", url, headers=token, params=params)
                result = json.loads(response.text)
                return result.get("result")

        else:
            return "Ключ 'operationAmount' отсутствует"
    else:
        return ""


if __name__ == "__main__":
    file_with_operations = os.path.join(os.path.dirname(os.path.dirname(__file__)), "data", "operations.json")
    operations_list = converting_data_into_a_dict_list(file_with_operations)
    get_amount = returns_the_transaction_amount(operations_list[1])
    print(get_amount)
############################################################################################