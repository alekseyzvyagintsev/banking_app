from typing import Union

from masks import get_mask_card_number
from masks import get_mask_account

def mask_account_card(account_card: Union[str, int]) -> str:
    if "Счет" in account_card:
        result = get_mask_account(int(account_card[-20:]))
        return f"{account_card[0:-20]}{result}"
    else:
        result = get_mask_card_number(int(account_card[-16:]))
        return f"{account_card[0:-16]}{result}"

