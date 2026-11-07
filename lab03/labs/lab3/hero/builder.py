from .hero import Hero
from .hero_class import HeroClass


class HeroBuilder:
    """Builder: constructs a Hero step by step and validates required fields."""
    def __init__(self):
        self._name = None
        self._hero_class = None
        self._weapon = None
        self._armor = None
        self._level = 1
        self._gold = Hero.STARTING_GOLD

    def set_name(self, name):
        self._name = name
        return self

    def set_hero_class(self, hero_class: HeroClass):
        self._hero_class = hero_class
        return self

    def set_weapon(self, weapon):
        self._weapon = weapon
        return self

    def set_armor(self, armor):
        self._armor = armor
        return self

    def set_starter_kit(self, starter_kit):
        self._weapon = starter_kit.create_weapon()
        self._armor = starter_kit.create_armor()
        return self

    def set_level(self, level):
        self._level = level
        return self

    def set_gold(self, gold):
        self._gold = gold
        return self

    def build(self):
        if not isinstance(self._name, str) or not self._name.strip():
            raise ValueError("У героя должно быть имя")
        if len(self._name.strip()) > Hero.MAX_NAME_LENGTH:
            raise ValueError(f"Имя героя не может быть длиннее {Hero.MAX_NAME_LENGTH} символов")
        if self._hero_class is None:
            raise ValueError("Не выбран класс героя")
        if self._weapon is None or self._armor is None:
            raise ValueError("Герою нужны оружие и броня")
        if self._level < 1:
            raise ValueError("Уровень героя не может быть меньше 1")
        if self._gold < 0:
            raise ValueError("Золота не может быть меньше нуля")
        return Hero(self._name, self._hero_class, self._level, self._gold,
                    self._weapon, self._armor)
