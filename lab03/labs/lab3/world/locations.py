from ..enemies.enemies import Goblin, Skeleton, Dragon
from ..items.catalog import (
    GOBLIN_CLEAVER, HUNTING_BOW, LEATHER_ARMOR, KNIGHT_BLADE,
    BONE_BOW, NECROMANCER_STAFF, CRYPT_MAIL, DAWN_BLADE, DRAGONSCALE_ARMOR
)
from .location import Location


class Forest(Location):
    def __init__(self, catalog):
        super().__init__("forest", "Мистический лес", 1, catalog)
    def _create_enemy(self): return Goblin()
    @property
    def _loot_table(self):
        return (GOBLIN_CLEAVER, HUNTING_BOW, LEATHER_ARMOR)


class Crypt(Location):
    def __init__(self, catalog):
        super().__init__("crypt", "Заброшенный склеп", 3, catalog)
    def _create_enemy(self): return Skeleton()
    @property
    def _loot_table(self):
        return (KNIGHT_BLADE, BONE_BOW, NECROMANCER_STAFF, CRYPT_MAIL)


class DragonLair(Location):
    def __init__(self, catalog):
        super().__init__("dragon-lair", "Логово дракона", 5, catalog)
    def _create_enemy(self): return Dragon()
    @property
    def _loot_table(self):
        return (DAWN_BLADE, DRAGONSCALE_ARMOR)
