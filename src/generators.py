from typing import Any, Generator, Iterable, Iterator, Optional


def filter_by_currency(
    list_of_actions: Iterable[dict[str, Any]], code: Optional[str] = None
) -> Iterator[Any] | list[dict[str, Any]]:
    """
    Фильтр списка транзакций по типу валюты.
    На вход принимает список транзакций.
    На выход отдает список транзакций.
    """
    if not list_of_actions:
        return iter([])  # Пустой итератор для пустого списка
    elif not code:
        return iter([])  # Пустой итератор для отсутствующего кода
    filtered_transactions = (
        transaction for transaction in list_of_actions if transaction["operationAmount"]["currency"]["code"] == code
    )
    if not filtered_transactions:
        raise ValueError("Транзакции с таким кодом валюты отсутствуют в списке.")
    return filtered_transactions


def transaction_descriptions(
    list_of_actions: Optional[Iterable[dict[str, Any]]] = None,
) -> Generator[Any, str | None, Iterator[Any] | None]:
    """
    Фильтр списка транзакций.
    На вход принимает список транзакций.
    На выход отдает список с описаниями транзакций.
    """
    if not list_of_actions:
        return None
    for action in list_of_actions:
        yield action["description"]
    return None


def card_number_generator(start: int = 1, stop: int = 9999999999999999) -> Generator[str, Any, None]:
    """
    Простой генератор номеров кредитных карт.
    На вход принимает два числа от 1 до 16-ти знаков.
    На выход отдает список номеров в указанном диапазоне,
    в формате "ХХХХ ХХХХ ХХХХ ХХХХ"
    """
    if start < stop and start <= 0:
        start = 1
        card_numbers_list = (
            f"{i[0:4]} {i[4:8]} {i[8:12]} {i[-4:]}" for i in ("{:016d}".format(i) for i in range(start, stop + 1))
        )
        return card_numbers_list
    elif start > stop:
        raise ValueError("Старт больше чем стоп")
    else:
        card_numbers_list = (
            f"{i[0:4]} {i[4:8]} {i[8:12]} {i[-4:]}" for i in ("{:016d}".format(i) for i in range(start, stop + 1))
        )
        return card_numbers_list


# if __name__ == '__main__':
#     from tests.transactions_data import transactions
#
#     usd_transactions = filter_by_currency(transactions, 'RUB')
#     for i in range(2):
#         print(next(usd_transactions))

# if __name__ == '__main__':
#     # from tests.transactions_data import transactions
#
#     descriptions = transaction_descriptions()
#     for _ in range(5):
#         print(next(iter(descriptions)))

# if __name__ == '__main__':
#     print(card_number_generator(6, 6))
