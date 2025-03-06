from src.generators import card_number_generator

for card_number in card_number_generator(1, 5):
    print(card_number)

# >>> 0000 0000 0000 0001
#     0000 0000 0000 0002
#     0000 0000 0000 0003
#     0000 0000 0000 0004
#     0000 0000 0000 0005