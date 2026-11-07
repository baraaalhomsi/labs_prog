from .enchantment import FOR_ARMOR
from .item import Item


class Armor(Item):
    MAX_DEFENSE = 0.75

    def __init__(self, code, name, base_price, defense):
        super().__init__(code, name, base_price)
        self._defense = defense

    @property
    def defense(self):
        bonus = sum(e.bonus_defense for e in self.enchantments)
        return min(self._defense + bonus, self.MAX_DEFENSE)

    @property
    def possible_enchantments(self):
        return FOR_ARMOR

    @property
    def description(self):
        return f"защита {round(self.defense * 100)}%"
