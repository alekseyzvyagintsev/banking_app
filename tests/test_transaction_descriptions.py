from src.generators import transaction_descriptions

from conftest import transactions


descriptions = transaction_descriptions(transactions)
for i in range(5):
    print(next(descriptions))

# >>> Перевод организации
#     Перевод со счета на счет
#     Перевод со счета на счет
#     Перевод с карты на карту
#     Перевод организации