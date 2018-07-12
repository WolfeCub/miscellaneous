import json
import random
from collection import Collection
from standard import Standard

collection = None
    
def handle_legendary(legendary, golden):
    choice = collection.get_legendary_not_in_collection(legendary)
    if choice is not None:
        collection.add_to_collection(choice, golden)

def handle_card(list, golden, message):
    choice = random.choice(list)
    collection.add_to_collection(choice, golden)

def generate_card(standard):
    rand = random.uniform(0, 100)
    if rand < 0.10:
        handle_legendary(standard.legendary, True)
    elif rand < 1.06:
        handle_legendary(standard.legendary, False)
    elif rand < 1.36:
        handle_card(standard.epic, True, 'EPIC')
    elif rand < 5.56:
        handle_card(standard.epic, False, 'EPIC')
    elif rand < 7.04:
        handle_card(standard.epic, True, 'RARE')
    elif rand < 28.71:
        handle_card(standard.epic, False, 'RARE')
    elif rand < 30.33:
        handle_card(standard.epic, True, 'RARE')
    else:
        handle_card(standard.epic, False, 'COMMON')

def main():
    global collection
    cards = json.loads(open('cards.collectible.json', encoding='utf8').read())
    standard_lst = [c for c in cards if (c['set'] in ['GILNEAS', 'LOOTAPALOOZA',
                                                    'EXPERT1', 'ICECROWN', 'UNGORO'])]

    standard = Standard(standard_lst)
    total = 0
    for i in range(0, 1000):
        collection = Collection(standard)
        counter = 0
        while collection.dust_remaining() > 0:
            generate_card(standard)
            counter += 1
        print(f'Trail #{i} - {counter/5}')
        total += counter/5

    print(f'Average: {total/1000}')

if __name__ == '__main__': main()
