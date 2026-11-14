from ..combat.combatant import Combatant
from ..combat.models import Hit
from ..core.dice import Dice
from ..items.weapon import Weapon
from .enemies import Enemy

class HauntedWeapon(Enemy):

    def __init__(self, weapon: Weapon):
        if not isinstance(weapon, Weapon):
            raise TypeError("HauntedWeapon requires a Weapon")

        self._weapon = weapon
        self._health = 100
        self._max_health = 100
        self._experience_reward = 40
        self._gold_reward = 25

    @property
    def code(self) -> str:
        return f"haunted-{self._weapon.code}"

    @property
    def name(self) -> str:
        return f"Haunted {self._weapon.name}"

    @property
    def health(self) -> int:
        return self._health

    @property
    def max_health(self) -> int:
        return self._max_health

    @property
    def experience_reward(self) -> int:
        return self._experience_reward

    def is_alive(self) -> bool:
        return self._health > 0

    def roll_damage(self) -> Hit:
        return self._weapon.roll_damage()

    def receive_hit(self, damage: int) -> int:
        dealt = max(1, damage)
        self._health = max(0, self._health - dealt)
        return dealt

    def roll_gold_reward(self) -> int:
        return Dice().roll(
            self._gold_reward // 2,
            self._gold_reward
        )