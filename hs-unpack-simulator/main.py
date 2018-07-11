import json
import random
from collection import Collection

TOTAL_LEGENDARIES = None

collection = None
    
def filter_rarity(rarity, list):
    return [c for c in list if c['rarity'] == rarity]

def handle_legendary(legendary, golden):
    if collection.legendary_count < TOTAL_LEGENDARIES:
        choice = collection.get_legendary_not_in_collection(legendary)
        collection.add_to_collection(choice, golden)

def handle_card(list, golden, message):
    choice = random.choice(list)
    collection.add_to_collection(choice, golden)

def generate_card(common, rare, epic, legendary):
    rand = random.uniform(0, 100)
    if rand < 0.10:
        handle_legendary(legendary, True)
    elif rand < 1.06:
        handle_legendary(legendary, False)
    elif rand < 1.36:
        handle_card(epic, True, 'EPIC')
    elif rand < 5.56:
        handle_card(epic, False, 'EPIC')
    elif rand < 7.04:
        handle_card(epic, True, 'RARE')
    elif rand < 28.71:
        handle_card(epic, False, 'RARE')
    elif rand < 30.33:
        handle_card(epic, True, 'RARE')
    else:
        handle_card(epic, False, 'COMMON')

def main():
    global collection
    cards = json.loads(open('cards.collectible.json', encoding='utf8').read())
    standard = [c for c in cards if (c['set'] in ['GILNEAS', 'LOOTAPALOOZA',
                                                'EXPERT1', 'ICECROWN', 'UNGORO'])]

    common = filter_rarity('COMMON', standard)
    rare = filter_rarity('RARE', standard)
    epic = filter_rarity('EPIC', standard)
    legendary = filter_rarity('LEGENDARY', standard)

    global TOTAL_LEGENDARIES
    TOTAL_LEGENDARIES = len(legendary)

    total = 0
    for i in range(0, 1000):
        collection = Collection(standard)
        counter = 0
        while collection.dust_remaining() > 0:
            generate_card(common, rare, epic, legendary)
            counter += 1
        print(f'Trail #{i} - {counter/5}')
        total += counter/5

    print(f'Average: {total/1000}')

if __name__ == '__main__': main()
