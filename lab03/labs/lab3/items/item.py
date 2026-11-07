from abc import ABC, abstractmethod
from copy import copy
from .enchantment import Enchantment


class Item(ABC):
    def __init__(self, code: str, name: str, base_price: int):
        self._code = code
        self._name = name
        self._base_price = base_price
        self._enchantments: list[Enchantment] = []

    def copy(self):
        # Prototype: shallow-copy the object, but give the clone its own mutable list.
        clone = copy(self)
        clone._enchantments = list(self._enchantments)
        return clone

    @property
    @abstractmethod
    def possible_enchantments(self): ...

    @property
    @abstractmethod
    def description(self) -> str: ...

    def enchant(self, enchantment: Enchantment):
        if enchantment not in self.possible_enchantments:
            raise ValueError(
                f"Зачарование '{enchantment.name}' не подходит для '{self.name}'"
            )
        self._enchantments.append(enchantment)

    @property
    def code(self): return self._code

    @property
    def name(self): return self._name

    @property
    def price(self):
        return self._base_price + sum(e.bonus_price for e in self._enchantments)

    @property
    def enchantments(self):
        return tuple(self._enchantments)
