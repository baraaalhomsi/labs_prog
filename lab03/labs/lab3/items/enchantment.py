from dataclasses import dataclass


@dataclass(frozen=True)
class Enchantment:
    code: str
    name: str
    bonus_damage: int = 0
    bonus_defense: float = 0.0
    bonus_price: int = 0


SHARP = Enchantment("sharp", "Острое", 3, 0, 20)
FIERY = Enchantment("fiery", "Огненное", 6, 0, 50)
STURDY = Enchantment("sturdy", "Прочное", 0, 0.05, 20)
WARDING = Enchantment("warding", "Охранное", 0, 0.10, 50)
FOR_WEAPONS = (SHARP, FIERY)
FOR_ARMOR = (STURDY, WARDING)
