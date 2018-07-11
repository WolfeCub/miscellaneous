import json
import random

DUSTING_MAP = {
    'COMMON': 5,
    'GOLDEN_COMMON': 50,
    'RARE': 20,
    'GOLDEN_RARE': 100,
    'EPIC': 100,
    'GOLDEN_EPIC': 400,
    'LEGENDARY': 400,
    'GOLDEN_LEGENDARY': 1600
}

TOTAL_LEGENDARIES = None
    
current_collection = {}
total_dust = 0
legendary_count = 0

def dust_remaining(standard):
    remaining = [v for v in standard if v['dbfId'] not in current_collection]
    total = 0
    for item in remaining:
        if item['rarity'] != 'LEGENDARY':
            total += DUSTING_MAP['GOLDEN_' + item['rarity']] * 2
        else:
            total += DUSTING_MAP['GOLDEN_' + item['rarity']]
    return total - total_dust

def add_to_collection(choice, golden):
    global current_collection
    count = current_collection.get(choice['dbfId'], 0)
    if count < 2:
        current_collection[choice['dbfId']] = count + 1
    else:
        return DUSTING_MAP[('GOLDEN_' if golden else '') + choice['rarity']]
    return 0

def get_legendary_not_in_collection(legendary):
    global legendary_count
    while True:
        choice = random.choice(legendary)
        if choice['dbfId'] not in current_collection:
            legendary_count += 1
            return choice

def filter_rarity(rarity, list):
    return [c for c in list if c['rarity'] == rarity]

def handle_legendary(legendary, golden):
    global total_dust, legendary_count
    if legendary_count < TOTAL_LEGENDARIES:
        choice = get_legendary_not_in_collection(legendary)
        add_to_collection(choice, golden)
        #print(f'LEGENDARY: {choice["name"]}\t\tDust: {total_dust}')
    else:
        total_dust += DUSTING_MAP[('GOLDEN_' if golden else '') + 'LEGENDARY']

def handle_card(list, golden, message):
    global total_dust
    choice = random.choice(list)
    total_dust += add_to_collection(choice, golden)
    #print(f'{message}: {choice["name"]}\t\tDust: {total_dust}')

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
    global total_dust, current_collection, legendary_count
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
        counter = 0
        while dust_remaining(standard) > 0:
            generate_card(common, rare, epic, legendary)
            counter += 1
        total_dust = 0
        current_collection = {}
        legendary_count = 0
        print(f'Trail #{i} - {counter/5}')
        total += counter/5

    print(f'Average: {total/1000}')


if __name__ == '__main__': main()
