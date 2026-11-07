from abc import ABC, abstractmethod
from ..items.catalog import (
    TRAINING_SWORD, CHAINMAIL, HUNTING_BOW, LEATHER_ARMOR,
    APPRENTICE_STAFF, LINEN_ROBE
)


class StarterKitFactory(ABC):
    """Abstract Factory: each concrete factory creates a weapon-and-armor family."""
    @abstractmethod
    def create_weapon(self): ...

    @abstractmethod
    def create_armor(self): ...


class WarriorKitFactory(StarterKitFactory):
    def __init__(self, catalog): self.catalog = catalog
    def create_weapon(self): return self.catalog.create_weapon(TRAINING_SWORD)
    def create_armor(self): return self.catalog.create_armor(CHAINMAIL)


class RangerKitFactory(StarterKitFactory):
    def __init__(self, catalog): self.catalog = catalog
    def create_weapon(self): return self.catalog.create_weapon(HUNTING_BOW)
    def create_armor(self): return self.catalog.create_armor(LEATHER_ARMOR)


class MageKitFactory(StarterKitFactory):
    def __init__(self, catalog): self.catalog = catalog
    def create_weapon(self): return self.catalog.create_weapon(APPRENTICE_STAFF)
    def create_armor(self): return self.catalog.create_armor(LINEN_ROBE)
