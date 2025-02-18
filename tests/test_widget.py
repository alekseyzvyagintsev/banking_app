from src.widget import mask_account_card, get_date

assert mask_account_card("Maestro 1596837868705199") == "Maestro 1596 83** **** 5199"
assert mask_account_card("Счет 64686473678894779589") == "Счет **9589"
assert mask_account_card("MasterCard 7158300734726758") == "MasterCard 7158 30** **** 6758"
assert mask_account_card("Visa Classic 6831982476737658") == "Visa Classic 6831 98** **** 7658"
assert mask_account_card("Visa Platinum 8990922113665229") == "Visa Platinum 8990 92** **** 5229"
assert mask_account_card("Visa Gold 5999414228426353") == "Visa Gold 5999 41** **** 6353"
assert mask_account_card("Visa Gold 5999414228426353 ")
assert mask_account_card("Visa Gold 599941422842635")
assert mask_account_card(["Visa Gold 5999414228426353"])
assert mask_account_card("Счет 64686473678894779589 ")
assert mask_account_card("Счет 6468647367889477958")
assert mask_account_card(["Счет 64686473678894779589"])
assert mask_account_card()


assert get_date("2024-03-11T02:26:18.671407")
assert get_date("2024-03-1102:26:18.671407")
assert get_date(["2024-03-11T02:26:18.67140"])
assert get_date()