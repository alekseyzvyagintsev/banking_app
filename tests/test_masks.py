import pytest

from src.masks import get_mask_card_number
from src.masks import get_mask_account


assert get_mask_card_number(1111111111111111) == "1111 11** **** 1111"
assert get_mask_card_number("1111111111111111")
assert get_mask_card_number(111111111111111)
assert get_mask_card_number(11111111111111111)


assert get_mask_account(11111111111111111111) == "**1111"
assert get_mask_account("11111111111111111111")
assert get_mask_account(1111111111111111111)
assert get_mask_account(111111111111111111111)
