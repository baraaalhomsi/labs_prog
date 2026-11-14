from ..combat.models import Hit
from .enemies import Enemy

class EnemyDecorator(Enemy):
    """
    Базовый декоратор для врагов.
    """

    def __init__(self, enemy: Enemy):
        self._enemy = enemy

    @property
    def code(self):
        return self._enemy.code

    @property
    def name(self):
        return self._enemy.name

    @property
    def health(self):
        return self._enemy.health

    @property
    def max_health(self):
        return self._enemy.max_health

    @property
    def experience_reward(self):
        return self._enemy.experience_reward

    def is_alive(self):
        return self._enemy.is_alive()

    def roll_damage(self):
        return self._enemy.roll_damage()

    def receive_hit(self, damage):
        return self._enemy.receive_hit(damage)

    def roll_gold_reward(self):
        return self._enemy.roll_gold_reward()

class LegendaryEnemy(EnemyDecorator):
    """
    Легендарный враг: наносит больше урона и дает больше наград.
    """

    @property
    def name(self):
        return f"Легендарный {self._enemy.name}"

    @property
    def experience_reward(self):
        return self._enemy.experience_reward * 2

    def roll_damage(self):
        hit = self._enemy.roll_damage()
        return Hit(hit.damage * 2, hit.critical)

    def roll_gold_reward(self):
        return self._enemy.roll_gold_reward() * 2

class WindfuryEnemy(EnemyDecorator):
    """
    Враг с яростью ветра: выполняет две атаки за один ход.
    """

    def roll_damage(self):
        first_hit = self._enemy.roll_damage()
        second_hit = self._enemy.roll_damage()

        total_damage = first_hit.damage + second_hit.damage
        critical = first_hit.critical or second_hit.critical

        return Hit(total_damage, critical)

class ArmoredEnemy(EnemyDecorator):
    """
    Бронированный враг: получает на 50% меньше урона.
    """

    @property
    def name(self):
        return f"Бронированный {self._enemy.name}"

    def receive_hit(self, damage):
        reduced_damage = max(1, round(damage * 0.5))
        return self._enemy.receive_hit(reduced_damage)