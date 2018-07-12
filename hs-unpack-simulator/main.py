import json
import random
from collection import Collection
from standard import Standard
from pprint import pprint

collection = None

def handle_card(list, golden, message):
    if message == 'LEGENDARY':
        choice = collection.get_legendary_not_in_collection(list)
    else:
        choice = random.choice(list)
    choice['isGolden'] = True if golden else False
    return choice

def generate_card(standard):
    rand = random.uniform(0, 100)
    if rand < 0.10:
        return handle_card(standard.legendary, True, 'LEGENDARY')
    elif rand < 1.06:
        return handle_card(standard.legendary, False, 'LEGENDARY')
    elif rand < 1.36:
        return handle_card(standard.epic, True, 'EPIC')
    elif rand < 5.56:
        return handle_card(standard.epic, False, 'EPIC')
    elif rand < 7.04:
        return handle_card(standard.rare, True, 'RARE')
    elif rand < 28.71:
        return handle_card(standard.rare, False, 'RARE')
    elif rand < 30.33:
        return handle_card(standard.common, True, 'COMMON')
    else:
        return handle_card(standard.common, False, 'COMMON')

def get_non_common_card(standard):
    c = generate_card(standard)
    while c['rarity'] != 'COMMON':
        c = generate_card(standard)
    return c

def generate_pack(standard):
    pack = [generate_card(standard) for x in range(5)]
    commons = [c for c in pack if c['rarity'] == 'COMMON']
    if len(commons) == 5:
        pack.pop()
        pack.append(get_non_common_card(standard))
    for c in pack:
        collection.add_to_collection(c, c['isGolden'])

def main():
    global collection
    cards = json.loads(open('cards.collectible.json', encoding='utf8').read())
    standard_lst = [c for c in cards if (c['set'] in ['GILNEAS', 'LOOTAPALOOZA',
                                                    'EXPERT1', 'ICECROWN', 'UNGORO'])]

    standard = Standard(standard_lst)
    runs = 100
    total = 0
    for i in range(0, runs):
        collection = Collection(standard)
        counter = 0
        while collection.dust_remaining() > 0:
            generate_pack(standard)
            counter += 1

        total += counter
        print(f'{i}/{runs}\t\t', end='\r')

    print(f'Average: {total/runs}')
    print(f'Cost: ${((total/runs)/60)*88:.2f} CAD')


if __name__ == '__main__': main()
