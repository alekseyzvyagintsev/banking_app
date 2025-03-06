from typing import Any, Iterable, Optional, Generator


def filter_by_currency(list_of_actions: Iterable[dict[str, Any]], code: Optional[str] = None
) -> str | Generator[dict[str, Any], Any, None]:
    if not list_of_actions:
        return "Список пуст"
    else:
        result: Generator[dict[str, Any], Any, None] = \
            (currency for currency in list_of_actions if currency['operationAmount']['currency']['code'] == code)
        return result


def transaction_descriptions(list_of_actions: Optional[Iterable[dict[str, Any]]] = None) -> Generator[
    Any, str | None, str | None]:

    if not list_of_actions:
        yield "Список пуст"
    else:
        for action in list_of_actions:
            yield action['description']


def card_number_generator(start: int=1, stop: int=None) -> Generator[str, Any, None]:
    card_numbers_dict = (f"{i[0:4]} {i[4:8]} {i[8:12]} {i[-4:]}" for i in (
        "{:016d}".format(i) for i in range(start, stop)))

    return card_numbers_dict


# if __name__ == '__main__':
#     from tests.transactions_data import transactions
#
    # usd_transactions = filter_by_currency(transactions, 'USD')
    # for i in range(2):
    #     print(next(usd_transactions))

# if __name__ == '__main__':
#     # from tests.transactions_data import transactions
#
#     descriptions = transaction_descriptions()
#     for _ in range(5):
#         print(next(iter(descriptions)))

# if __name__ == '__main__':
#     print(list(card_number_generator(1777, 1782)))