from abc import abstractmethod
from ..combat.models import Hit
from ..core.dice import Dice
from .enchantment import FOR_WEAPONS
from .item import Item


class Weapon(Item):
    def __init__(self, code, name, base_price, damage):
        super().__init__(code, name, base_price)
        self._damage = damage

    @abstractmethod
    def roll_damage(self) -> Hit: ...

    @property
    def damage(self):
        return self._damage + sum(e.bonus_damage for e in self.enchantments)

    @property
    def possible_enchantments(self):
        return FOR_WEAPONS


class Sword(Weapon):
    def roll_damage(self):
        return Hit(self.damage)

    @property
    def description(self):
        return f"урон {self.damage}"


class Bow(Weapon):
    def __init__(self, code, name, base_price, damage, critical_chance):
        super().__init__(code, name, base_price, damage)
        self._critical_chance = critical_chance

    def roll_damage(self):
        if Dice().chance(self._critical_chance):
            return Hit(self.damage * 2, True)
        return Hit(self.damage)

    @property
    def description(self):
        return f"урон {self.damage}, шанс крита {round(self._critical_chance * 100)}%"


class Staff(Weapon):
    def __init__(self, code, name, base_price, damage, scatter):
        super().__init__(code, name, base_price, damage)
        self._scatter = scatter

    @property
    def _min_damage(self):
        return round(self.damage * (1 - self._scatter))

    @property
    def _max_damage(self):
        return round(self.damage * (1 + self._scatter))

    def roll_damage(self):
        return Hit(Dice().roll(self._min_damage, self._max_damage))

    @property
    def description(self):
        return f"урон {self._min_damage}-{self._max_damage}"
