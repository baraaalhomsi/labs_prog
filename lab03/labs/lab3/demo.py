"""Console demonstrations of all five required creational patterns."""
from .core.dice import Dice
from .hero.builder import HeroBuilder
from .hero.hero_class import HeroClass
from .items.catalog import create_default_catalog, TRAINING_SWORD
from .items.enchantment import SHARP
from .kits.factories import WarriorKitFactory, RangerKitFactory
from .world.locations import Forest, Crypt


def run_demo():
    print("\n========== DEMO: FIVE DESIGN PATTERNS ==========")

    print("\n1) SINGLETON")
    first = Dice()
    second = Dice()
    print("Dice() is Dice():", first is second)
    print("Ожидается True: оба обращения возвращают один объект.")

    catalog = create_default_catalog()

    print("\n2) BUILDER")
    hero = (
        HeroBuilder()
        .set_name("Артур")
        .set_hero_class(HeroClass.WARRIOR)
        .set_starter_kit(HeroClass.WARRIOR.get_starter_kit(catalog))
        .build()
    )
    print(f"Создан герой: {hero.name}, класс: {hero.hero_class.display_name}, "
          f"здоровье: {hero.max_health}, золото: {hero.gold}")

    print("\n3) FACTORY METHOD")
    forest_enemy = Forest(catalog)._create_enemy()
    crypt_enemy = Crypt(catalog)._create_enemy()
    print(f"Forest создает: {forest_enemy.name} ({forest_enemy.code})")
    print(f"Crypt создает: {crypt_enemy.name} ({crypt_enemy.code})")

    print("\n4) ABSTRACT FACTORY")
    warrior_factory = WarriorKitFactory(catalog)
    ranger_factory = RangerKitFactory(catalog)
    print("Воин:", warrior_factory.create_weapon().name, "+", warrior_factory.create_armor().name)
    print("Следопыт:", ranger_factory.create_weapon().name, "+", ranger_factory.create_armor().name)

    print("\n5) PROTOTYPE")
    original = catalog.create(TRAINING_SWORD)
    clone = original.copy()
    clone.enchant(SHARP)
    print("Оригинал:", original.name, "|", original.description, "| цена", original.price)
    print("Копия:   ", clone.name, "|", clone.description, "| цена", clone.price)
    print("Список зачарований независим:", original.enchantments != clone.enchantments)
    print("Каталожный шаблон не изменился:", catalog.create(TRAINING_SWORD).price == original.price)

    print("\n========== END OF DEMO ==========\n")


if __name__ == "__main__":
    run_demo()
