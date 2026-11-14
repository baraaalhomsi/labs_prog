from .items.catalog import (
    create_default_catalog,
    IRON_SWORD,
    ELVEN_BOW,
    EMBER_STAFF,
    CHAINMAIL,
    PLATE_ARMOR
)

from .world.locations import Forest, Crypt, DragonLair
from .world.registry import LocationRegistry
from .camp.merchant import Merchant
from .hero.builder import HeroBuilder
from .hero.hero_class import HeroClass

class GameFacade:
    """
    Фасад: предоставляет простой интерфейс
    для взаимодействия с подсистемами игры.
    """

    def __init__(self):
        # Создание каталога предметов
        self._catalog = create_default_catalog()

        # Создание и регистрация локаций
        self._locations = LocationRegistry([
            Forest(self._catalog),
            Crypt(self._catalog),
            DragonLair(self._catalog)
        ])

        # Создание торговца
        self._merchant = Merchant(
            self._catalog,
            [
                IRON_SWORD,
                ELVEN_BOW,
                EMBER_STAFF,
                CHAINMAIL,
                PLATE_ARMOR
            ]
        )

    def create_hero(self, name, hero_class=HeroClass.WARRIOR):
        """
        Создает героя вместе со стартовым снаряжением.
        """
        return (
            HeroBuilder()
            .set_name(name)
            .set_hero_class(hero_class)
            .set_starter_kit(
                hero_class.get_starter_kit(self._catalog)
            )
            .build()
        )

    def get_locations(self):
        """
        Возвращает список доступных локаций.
        """
        return self._locations.get_all()

    def get_location(self, code):
        """
        Возвращает локацию по коду.
        """
        return self._locations.get(code)

    def explore(self, hero, location_code, seed=None):
        """
        Отправляет героя на исследование локации.
        """
        location = self.get_location(location_code)
        return location.explore(hero, seed)

    @property
    def merchant(self):
        return self._merchant

    @property
    def catalog(self):
        return self._catalog