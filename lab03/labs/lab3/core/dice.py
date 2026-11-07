import random
from typing import Sequence, TypeVar

T = TypeVar("T")


class Dice:
    """Singleton: one reproducible random source for the whole game."""
    _instance = None

    def __new__(cls):
        if cls._instance is None:
            cls._instance = super().__new__(cls)
            cls._instance._random = random.Random()
        return cls._instance

    def reseed(self, seed: int) -> None:
        self._random.seed(seed)

    def next_seed(self) -> int:
        return self._random.randrange(1_000_000)

    def roll(self, low: int, high: int) -> int:
        if low > high:
            raise ValueError("low must not exceed high")
        return self._random.randint(low, high)

    def chance(self, probability: float) -> bool:
        if not 0 <= probability <= 1:
            raise ValueError("probability must be between 0 and 1")
        return self._random.random() < probability

    def pick(self, options: Sequence[T]) -> T:
        if not options:
            raise ValueError("options cannot be empty")
        return self._random.choice(options)
