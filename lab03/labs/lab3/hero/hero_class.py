from enum import Enum
from ..kits.factories import WarriorKitFactory, RangerKitFactory, MageKitFactory


class HeroClass(Enum):
    WARRIOR = ("warrior", "Воин", 120, WarriorKitFactory)
    RANGER = ("ranger", "Следопыт", 100, RangerKitFactory)
    MAGE = ("mage", "Маг", 85, MageKitFactory)

    def __init__(self, code, display_name, base_health, factory_class):
        self.code = code
        self.display_name = display_name
        self.base_health = base_health
        self._factory_class = factory_class

    def get_starter_kit(self, catalog):
        return self._factory_class(catalog)
