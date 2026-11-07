from abc import ABC, abstractmethod
from .models import Hit


class Combatant(ABC):
    @property
    @abstractmethod
    def code(self) -> str: ...

    @property
    @abstractmethod
    def name(self) -> str: ...

    @property
    @abstractmethod
    def health(self) -> int: ...

    @property
    @abstractmethod
    def max_health(self) -> int: ...

    @abstractmethod
    def is_alive(self) -> bool: ...

    @abstractmethod
    def roll_damage(self) -> Hit: ...

    @abstractmethod
    def receive_hit(self, damage: int) -> int: ...
