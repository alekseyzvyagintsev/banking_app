############################################################################
from typing import Any, Iterable, Optional


def filter_by_state(
    list_of_actions: Iterable[dict[str, Any]], state: Optional[str] = "EXECUTED"
) -> list[dict[str, Any]]:
    """
    принимает список словарей и опционально значение для ключа state (по умолчанию 'EXECUTED').
    Функция возвращает новый список словарей, содержащий только те словари, у которых ключ state
    соответствует указанному значению.
    """
    result = list(filter(lambda i: i["state"] == state, list_of_actions))
    return result


def sort_by_date(list_of_actions: Iterable[dict[str, Any]], descending: bool = True) -> list[dict[str, Any]]:
    """
    принимает список словарей и необязательный параметр,
    задающий порядок сортировки (по умолчанию — убывание).
    Функция возвращает новый список, отсортированный по дате (date).
    """
    sorted_list = sorted(list_of_actions, key=lambda x: x["date"], reverse=descending)
    return sorted_list


############################################################################
