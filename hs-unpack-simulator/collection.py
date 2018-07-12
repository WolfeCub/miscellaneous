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
    def __init__(self, standard):
        self.current_collection = {}
        self.total_dust = 0
        self.legendary_count = 0
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

    def add_to_collection(self, choice, golden):
        count = self.current_collection.get(choice['dbfId'], 0)
        amount = 1 if choice['rarity'] == 'LEGENDARY' else 2
        if count < amount:
            self.current_collection[choice['dbfId']] = count + 1
            self._total_dust_cost -= DUSTING_MAP['GOLDEN_' + choice['rarity']]
        else:
            amount = DUSTING_MAP[('GOLDEN_' if golden else '') + choice['rarity']]
            self.update_dust(amount)

    def get_legendary_not_in_collection(self, legendary):
        self.legendary_count += 1
        try:
            random = self._legendary_pool.pop()
        except KeyError:
            return self._standard.legendary[0]
        return self._standard.lookup[random]
