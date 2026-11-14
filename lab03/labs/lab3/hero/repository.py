from abc import ABC, abstractmethod

from .hero import Hero

class HeroRepository(ABC):

    @abstractmethod
    def find_by_name(self, name: str):
        pass

    @abstractmethod
    def save(self, hero: Hero):
        pass

    @abstractmethod
    def delete(self, name: str):
        pass

class InMemoryHeroRepository(HeroRepository):

    def __init__(self):
        self._heroes = {}
        self.read_count = 0

    def find_by_name(self, name: str):
        self.read_count += 1
        return self._heroes.get(name)

    def save(self, hero: Hero):
        self._heroes[hero.name] = hero

    def delete(self, name: str):
        return self._heroes.pop(name, None)

class CachingHeroRepository(HeroRepository):

    def __init__(self, repository: HeroRepository):
        self._repository = repository
        self._cache = {}
        self.cache_hits = 0
        self.cache_misses = 0

    def find_by_name(self, name: str):
        if name in self._cache:
            self.cache_hits += 1
            return self._cache[name]

        self.cache_misses += 1
        hero = self._repository.find_by_name(name)

        if hero is not None:
            self._cache[name] = hero

        return hero

    def save(self, hero: Hero):
        self._repository.save(hero)
        self._cache[hero.name] = hero

    def delete(self, name: str):
        self._cache.pop(name, None)
        return self._repository.delete(name)