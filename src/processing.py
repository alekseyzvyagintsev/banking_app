
def filter_by_state(list_of_dict: list[dict], state='EXECUTED') -> list[dict]:
    '''
    принимает список словарей и опционально значение для ключа state (по умолчанию 'EXECUTED').
    Функция возвращает новый список словарей, содержащий только те словари, у которых ключ state
    соответствует указанному значению.
    '''
    result = list(filter(lambda i: i["state"] == state, list_of_dict))
    return result


