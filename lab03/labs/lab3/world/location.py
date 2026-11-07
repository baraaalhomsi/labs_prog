from abc import ABC, abstractmethod
from dataclasses import dataclass
from ..combat.battle import Battle
from ..combat.models import Outcome
from ..core.dice import Dice
from ..enemies.enemies import Enemy
from ..items.item import Item


@dataclass(frozen=True)
class Rewards:
    experience: int
    gold: int
    loot: Item | None
    levels_gained: int


@dataclass(frozen=True)
class ExpeditionReport:
    seed: int
    location_code: str
    battle: object
    rewards: Rewards


class Location(ABC):
    LOOT_CHANCE = 0.60
    ENCHANT_CHANCE = 0.30

    def __init__(self, code, display_name, recommended_level, catalog):
        self._code = code
        self._display_name = display_name
        self._recommended_level = recommended_level
        self._catalog = catalog

    @abstractmethod
    def _create_enemy(self) -> Enemy: ...

    @property
    @abstractmethod
    def _loot_table(self) -> tuple[str, ...]: ...

    @property
    def code(self): return self._code
    @property
    def display_name(self): return self._display_name
    @property
    def recommended_level(self): return self._recommended_level

    def explore(self, hero, seed=None):
        dice = Dice()
        actual_seed = dice.next_seed() if seed is None else seed
        dice.reseed(actual_seed)
        hero.restore_health()
        enemy = self._create_enemy()
        battle_report = Battle(hero, enemy).run()
        if battle_report.outcome == Outcome.VICTORY:
            rewards = self._reward(hero, enemy, dice)
        else:
            rewards = self._punish(hero)
        return ExpeditionReport(actual_seed, self._code, battle_report, rewards)

    def _reward(self, hero, enemy, dice):
        experience = enemy.experience_reward
        gold = enemy.roll_gold_reward()
        loot = self._roll_loot(dice)
        levels_gained = hero.gain_experience(experience)
        hero.add_gold(gold)
        if loot is not None:
            hero.add_item(loot)
        return Rewards(experience, gold, loot, levels_gained)

    def _roll_loot(self, dice):
        if not dice.chance(self.LOOT_CHANCE):
            return None
        code = dice.pick(self._loot_table)
        item = self._catalog.create(code)
        if dice.chance(self.ENCHANT_CHANCE) and item.possible_enchantments:
            item.enchant(dice.pick(item.possible_enchantments))
        return item

    def _punish(self, hero):
        lost_gold = hero.gold // 2
        hero.add_gold(-lost_gold)
        return Rewards(0, -lost_gold, None, 0)
