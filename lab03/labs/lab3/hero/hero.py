from ..combat.combatant import Combatant
from ..combat.models import Hit
from ..items.armor import Armor
from ..items.item import Item
from ..items.weapon import Weapon
from .hero_class import HeroClass
from ..core.events import Event, EventManager

class Hero(Combatant):
    MAX_NAME_LENGTH = 20
    STARTING_GOLD = 50
    HEALTH_PER_LEVEL = 15
    DAMAGE_PER_LEVEL = 3
    EXPERIENCE_PER_LEVEL = 100

    def __init__(self, name, hero_class, level, gold, weapon, armor):
        self._name = name.strip()
        self._hero_class = hero_class
        self._level = level
        self._experience = 0
        self._gold = gold
        self._weapon = weapon
        self._armor = armor
        self._inventory: list[Item] = []
        self._events = EventManager()
        self._health = self.max_health

    @property
    def code(self): return self._hero_class.code
    @property
    def name(self): return self._name
    @property
    def health(self): return self._health
    @property
    def max_health(self):
        return self._hero_class.base_health + (self._level - 1) * self.HEALTH_PER_LEVEL
    @property
    def hero_class(self): return self._hero_class
    @property
    def level(self): return self._level
    @property
    def experience(self): return self._experience
    @property
    def experience_to_next_level(self): return self._level * self.EXPERIENCE_PER_LEVEL
    @property
    def gold(self): return self._gold
    @property
    def weapon(self): return self._weapon
    @property
    def armor(self): return self._armor
    @property
    def inventory(self): return tuple(self._inventory)

    def is_alive(self): return self._health > 0

    def roll_damage(self):
        hit = self._weapon.roll_damage()
        return Hit(hit.damage + (self._level - 1) * self.DAMAGE_PER_LEVEL, hit.critical)

    def receive_hit(self, damage):
        dealt = max(1, round(damage * (1 - self._armor.defense)))
        self._health = max(0, self._health - dealt)
        return dealt

    def restore_health(self):
        self._health = self.max_health

    def gain_experience(self, amount):
        if amount < 0:
            raise ValueError("Опыт не может быть отрицательным")

        self._experience += amount
        gained = 0

        while self._experience >= self.experience_to_next_level:
            self._experience -= self.experience_to_next_level
            self._level += 1
            gained += 1

        if gained > 0:
            self._events.notify(
                Event(
                    "level_up",
                    {
                        "name": self.name,
                        "level": self.level,
                        "levels_gained": gained
                    }
                )
            )

        return gained

    def add_gold(self, amount):
        if self._gold + amount < 0:
            raise ValueError("Золота не может быть меньше нуля")
        self._gold += amount

    def spend_gold(self, amount):
        if amount < 0:
            raise ValueError("Сумма не может быть отрицательной")
        if amount > self._gold:
            raise ValueError(f"Не хватает золота: нужно {amount}, есть {self._gold}")
        self._gold -= amount

    def add_item(self, item):
        self._inventory.append(item)

        self._events.notify(
            Event(
                "item_added",
                {
                    "name": self.name,
                    "item": item.name
                }
            )
        )

    def remove_item(self, item):
        if item not in self._inventory:
            raise ValueError(f"В инвентаре нет предмета {item.name}")
        self._inventory.remove(item)

    def equip(self, item):
        if isinstance(item, Weapon):
            self.remove_item(item)
            self._inventory.append(self._weapon)
            self._weapon = item
        elif isinstance(item, Armor):
            self.remove_item(item)
            self._inventory.append(self._armor)
            self._armor = item
        else:
            raise ValueError(f"Предмет нельзя экипировать: {item.name}")

    def subscribe(self, observer):
        self._events.subscribe(observer)

    def unsubscribe(self, observer):
        self._events.unsubscribe(observer)
