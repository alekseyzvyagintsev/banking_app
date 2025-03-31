############################################################################
import re
from typing import Any, Iterable, Optional


def filter_by_state(
    list_of_actions: list[dict[str, Any]], state: Optional[str] = "EXECUTED"
) -> list[Any]:
    """
    принимает список словарей и опционально значение для ключа state (по умолчанию 'EXECUTED').
    Функция возвращает новый список словарей, содержащий только те словари, у которых ключ state
    соответствует указанному значению.
    """
    if not state:
        state = "EXECUTED"
    if any(state in dict_from_list.values() for dict_from_list in list_of_actions):
        result = [d for d in list_of_actions if d.get('state') == state]
        return result
    else:
        return []

def sort_by_date(list_of_actions: Iterable[dict[str, Any]], descending: Optional[bool] = True) -> list[dict[str, Any]]:
    """
    принимает список словарей и необязательный параметр,
    задающий порядок сортировки (по умолчанию — убывание).
    Функция возвращает новый список, отсортированный по дате (date).
    """
    if descending is not False:
        descending = True
    sorted_list = sorted(list_of_actions, key=lambda x: x["date"], reverse=descending)
    return sorted_list


def filter_by_description(list_of_actions: Iterable[dict[str, Any]], search_word: str) -> list[dict[str, Any]] | None:
    """
    Функция принимает список словарей и слово для фильтрации списка транзакций,
    Функция возвращает новый список, отсортированный по предложенному слову.
    """
    if search_word:
        # Регулярное выражение для поиска слова в любом месте строки
        pattern = f".*{search_word}.*"

        filtered_list = []
        for action_dict in list_of_actions:
            if re.search(pattern, action_dict['description'], re.IGNORECASE):
                filtered_list.append(action_dict)

        return filtered_list
    else:
        return []


############################################################################
