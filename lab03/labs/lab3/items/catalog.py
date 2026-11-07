from ..core.errors import UnknownCodeError
from .armor import Armor
from .item import Item
from .weapon import Sword, Bow, Staff, Weapon


# Stable item codes are used by factories, locations and the merchant.
TRAINING_SWORD = "training-sword"
HUNTING_BOW = "hunting-bow"
APPRENTICE_STAFF = "apprentice-staff"
CHAINMAIL = "chainmail"
LEATHER_ARMOR = "leather-armor"
LINEN_ROBE = "linen-robe"
IRON_SWORD = "iron-sword"
ELVEN_BOW = "elven-bow"
EMBER_STAFF = "ember-staff"
PLATE_ARMOR = "plate-armor"
GOBLIN_CLEAVER = "goblin-cleaver"
KNIGHT_BLADE = "knight-blade"
BONE_BOW = "bone-bow"
NECROMANCER_STAFF = "necromancer-staff"
CRYPT_MAIL = "crypt-mail"
DAWN_BLADE = "dawn-blade"
DRAGONSCALE_ARMOR = "dragonscale-armor"


class ItemCatalog:
    """Stores prototypes and returns independent copies."""
    def __init__(self):
        self._prototypes: dict[str, Item] = {}

    def register(self, prototype: Item):
        if prototype.code in self._prototypes:
            raise ValueError(f"Предмет '{prototype.code}' уже зарегистрирован")
        self._prototypes[prototype.code] = prototype

    def create(self, code: str) -> Item:
        prototype = self._prototypes.get(code)
        if prototype is None:
            raise UnknownCodeError("Предмет", code)
        return prototype.copy()

    def create_weapon(self, code: str) -> Weapon:
        item = self.create(code)
        if not isinstance(item, Weapon):
            raise ValueError(f"Предмет '{code}' не является оружием")
        return item

    def create_armor(self, code: str) -> Armor:
        item = self.create(code)
        if not isinstance(item, Armor):
            raise ValueError(f"Предмет '{code}' не является броней")
        return item

    @property
    def codes(self):
        return tuple(self._prototypes)


def create_default_catalog() -> ItemCatalog:
    catalog = ItemCatalog()
    prototypes = [
        Sword(TRAINING_SWORD, "Тренировочный меч", 20, 12),
        Bow(HUNTING_BOW, "Охотничий лук", 20, 10, 0.30),
        Staff(APPRENTICE_STAFF, "Посох ученика", 20, 14, 0.30),
        Armor(CHAINMAIL, "Кольчуга", 40, 0.30),
        Armor(LEATHER_ARMOR, "Кожаная броня", 30, 0.20),
        Armor(LINEN_ROBE, "Льняная роба", 15, 0.10),
        Sword(IRON_SWORD, "Железный меч", 80, 17),
        Bow(ELVEN_BOW, "Эльфийский лук", 90, 15, 0.35),
        Staff(EMBER_STAFF, "Посох углей", 95, 19, 0.25),
        Armor(PLATE_ARMOR, "Латный доспех", 100, 0.45),
        Sword(GOBLIN_CLEAVER, "Тесак гоблина", 35, 13),
        Sword(KNIGHT_BLADE, "Клинок рыцаря", 120, 22),
        Bow(BONE_BOW, "Костяной лук", 110, 18, 0.30),
        Staff(NECROMANCER_STAFF, "Посох некроманта", 125, 23, 0.30),
        Armor(CRYPT_MAIL, "Криптовая броня", 115, 0.40),
        Sword(DAWN_BLADE, "Клинок рассвета", 180, 28),
        Armor(DRAGONSCALE_ARMOR, "Драконья броня", 190, 0.55),
    ]
    for prototype in prototypes:
        catalog.register(prototype)
    return catalog
