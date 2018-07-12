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

class Collection:
    current_collection = {}
    total_dust = 0
    legendary_count = 0

    def __init__(self, standard):
        self._standard = standard

        total = 0
        for item in standard.all:
            if item['rarity'] != 'LEGENDARY':
                total += DUSTING_MAP['GOLDEN_' + item['rarity']] * 2
            else:
                total += DUSTING_MAP['GOLDEN_' + item['rarity']]
        self._total_dust_cost = total
        self._legendary_pool = set(c['dbfId'] for c in standard.legendary)

    def dust_remaining(self):
        return self._total_dust_cost - self.total_dust

    def update_dust(self, amount):
        self.total_dust += amount
        self._total_dust_cost -= amount

    def add_to_collection(self, choice, golden):
        count = self.current_collection.get(choice['dbfId'], 0)
        amount = 1 if choice['rarity'] == 'LEGENDARY' else 2
        if count < amount:
            self.current_collection[choice['dbfId']] = count + 1
        else:
            self.update_dust(DUSTING_MAP[('GOLDEN_' if golden else '')
                                         + choice['rarity']])

    def get_legendary_not_in_collection(self, legendary):
        self.legendary_count += 1
        try:
            random = self._legendary_pool.pop()
        except KeyError:
            return None
        return self._standard.lookup[random]
