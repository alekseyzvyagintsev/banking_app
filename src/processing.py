############################################################################
import re
from typing import Any, Iterable, Optional


def filter_by_state(list_of_actions: list[dict[str, Any]], state: Optional[str] = "EXECUTED") -> list[Any]:
    """
    принимает список словарей и опционально значение для ключа state (по умолчанию 'EXECUTED').
    Функция возвращает новый список словарей, содержащий только те словари, у которых ключ state
    соответствует указанному значению.
    """
    if not state:
        state = "EXECUTED"
    if any(state in dict_from_list.values() for dict_from_list in list_of_actions):
        result = [d for d in list_of_actions if d.get("state") == state]
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


def filter_by_description(
    list_of_actions: Iterable[dict[str, Any]], search_string: str
) -> list[dict[str, Any]] | None:
    """
    Функция принимает список словарей и слово для фильтрации списка транзакций,
    Функция возвращает новый список, отсортированный по предложенному слову.
    """
    if search_string:
        # Разделяем строку поиска на отдельные слова
        words = [word.lower() for word in search_string.split()]

        # Создаем регулярное выражение для каждого слова
        patterns = [re.compile(rf"\b{word}\b", flags=re.IGNORECASE) for word in words]

        filtered_list = []
        try:
            for transaction in list_of_actions:
                if all(
                    any(pattern.search(transaction.get("description", "")) for pattern in patterns)
                    for _ in range(len(patterns))
                ):
                    filtered_list.append(transaction)

            return filtered_list
        except Exception:
            print(f"Не найдено ни одной транзакции со словом(ами) {search_string}")
            return filtered_list
    else:
        return []


############################################################################
