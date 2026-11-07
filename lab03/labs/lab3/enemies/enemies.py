from abc import ABC, abstractmethod
from ..combat.combatant import Combatant
from ..combat.models import Hit
from ..core.dice import Dice


class Enemy(Combatant, ABC):
    @property
    @abstractmethod
    def experience_reward(self) -> int: ...

    @abstractmethod
    def roll_gold_reward(self) -> int: ...


class AbstractEnemy(Enemy):
    def __init__(self, code, name, max_health, min_damage, max_damage,
                 experience_reward, gold_reward):
        self._code = code
        self._name = name
        self._max_health = max_health
        self._min_damage = min_damage
        self._max_damage = max_damage
        self._experience_reward = experience_reward
        self._gold_reward = gold_reward
        self._health = max_health

    @property
    def code(self): return self._code
    @property
    def name(self): return self._name
    @property
    def health(self): return self._health
    @property
    def max_health(self): return self._max_health
    @property
    def experience_reward(self): return self._experience_reward

    def is_alive(self): return self._health > 0

    def roll_damage(self):
        return Hit(Dice().roll(self._min_damage, self._max_damage))

    def receive_hit(self, damage):
        dealt = max(1, self._reduce_damage(damage))
        self._health = max(0, self._health - dealt)
        return dealt

    def _reduce_damage(self, damage):
        return damage

    def roll_gold_reward(self):
        return Dice().roll(self._gold_reward // 2, self._gold_reward)


class Goblin(AbstractEnemy):
    def __init__(self):
        super().__init__("goblin", "Гоблин", 50, 6, 14, 40, 30)


class Skeleton(AbstractEnemy):
    RESISTANCE = 0.30
    def __init__(self):
        super().__init__("skeleton", "Скелет", 110, 10, 24, 90, 70)
    def _reduce_damage(self, damage):
        return round(damage * (1 - self.RESISTANCE))


class Dragon(AbstractEnemy):
    RESISTANCE = 0.25
    FIRE_BREATH_CHANCE = 0.25
    FIRE_BREATH_MULTIPLIER = 2

    def __init__(self):
        super().__init__("dragon", "Дракон", 260, 16, 22, 500, 400)

    def roll_damage(self):
        ordinary_hit = super().roll_damage()
        if Dice().chance(self.FIRE_BREATH_CHANCE):
            return Hit(ordinary_hit.damage * self.FIRE_BREATH_MULTIPLIER, True)
        return ordinary_hit

    def _reduce_damage(self, damage):
        return round(damage * (1 - self.RESISTANCE))
