######################################################################################
from typing import Any, Generator, Iterable, Iterator, Optional


def filter_by_currency(
    list_of_actions: Iterable[dict[str, Any]], currency_code: Optional[str] = None
) -> Iterator[Any] | list[dict[str, Any]]:
    """
    Фильтр списка транзакций по типу валюты.
    На вход принимает список транзакций.
    На возвращает отфильтрованный список транзакций.
    """

    def find_currency_in_transaction(transaction):
        """Рекурсивная функция для поиска валюты в словаре транзакции."""
        stack = [transaction]

        while stack:
            item = stack.pop()
            if isinstance(item, dict):  # Проверяем, является ли элемент словарем
                if "currency" in item and "code" in item["currency"]:
                    if item["currency"]["code"] == currency_code:
                        return True
                else:
                    stack.extend(item.values())  # Добавляем значения словаря в стек
            elif isinstance(item, list):  # Проверяем, является ли элемент списком
                stack.extend(item)  # Добавляем элементы списка в стек

        return False

    filtered_list = [transaction for transaction in list_of_actions if find_currency_in_transaction(transaction)]
    return list(filtered_list)


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


######################################################################################
