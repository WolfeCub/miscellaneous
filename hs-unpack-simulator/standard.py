class Standard:
    def filter_rarity(self, rarity, list):
        return [c for c in list if c['rarity'] == rarity]

    def __init__(self, standard):
        self.all = standard
        self.lookup = {c['dbfId']:c for c in standard}
        self.common = self.filter_rarity('COMMON', standard)
        self.rare = self.filter_rarity('RARE', standard)
        self.epic = self.filter_rarity('EPIC', standard)
        self.legendary = self.filter_rarity('LEGENDARY', standard)

