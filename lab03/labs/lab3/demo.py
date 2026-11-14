"""Console demonstrations of all five required creational patterns."""
from .core.dice import Dice
from .hero.builder import HeroBuilder
from .hero.hero_class import HeroClass
from .items.catalog import create_default_catalog, TRAINING_SWORD
from .items.enchantment import SHARP
from .kits.factories import WarriorKitFactory, RangerKitFactory
from .world.locations import Forest, Crypt
from .enemies.adapter import HauntedWeapon
from .enemies.enemies import Enemy
from .combat.battle import Battle
from .enemies.enemies import Goblin
from .enemies.decorators import (LegendaryEnemy, WindfuryEnemy, ArmoredEnemy)
from .hero.repository import (InMemoryHeroRepository, CachingHeroRepository)
from .game_facade import GameFacade
from .world.experience_strategy import (StandardExperienceStrategy, DoubleExperienceStrategy)
from .enemies.enemies import Goblin
from .core.observers import ConsoleObserver, AchievementObserver
from .hero.validation import (NameValidationHandler, ClassValidationHandler, StarterKitValidationHandler)

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

    print("\n6) ADAPTER")

    weapon = catalog.create_weapon(TRAINING_SWORD)
    haunted_weapon = HauntedWeapon(weapon)

    print("Исходный объект:", weapon.name)
    print("Адаптированный объект:", haunted_weapon.name)
    print("Является Enemy:", isinstance(haunted_weapon, Enemy))
    print("Здоровье:", haunted_weapon.health)
    print("Урон:", haunted_weapon.roll_damage().damage)

    haunted_weapon.receive_hit(20)

    print("Здоровье после получения урона:", haunted_weapon.health)

    print("\n7) DECORATOR")

    goblin = Goblin()

    legendary = LegendaryEnemy(goblin)

    print("\nОбычный враг:", goblin.name)
    print("Легендарный враг:", legendary.name)
    print("Обычная награда опыта:", goblin.experience_reward)
    print("Легендарная награда опыта:", legendary.experience_reward)

    windfury = WindfuryEnemy(Goblin())
    armored = ArmoredEnemy(Goblin())

    print("\nУрон обычного врага:", Goblin().roll_damage().damage)
    print("Урон врага с Windfury:", windfury.roll_damage().damage)

    print("\nЗдоровье бронированного врага:", armored.health)
    armored.receive_hit(20)
    print("Здоровье после получения урона:", armored.health)

    combined = ArmoredEnemy(
        WindfuryEnemy(
            LegendaryEnemy(Goblin())
        )
    )

    print("\nКомбинированный декоратор:", combined.name)
    print("Здоровье:", combined.health)
    print("Награда опыта:", combined.experience_reward)

    print("\n8) PROXY")

    real_repository = InMemoryHeroRepository()

    real_repository.save(hero)

    proxy = CachingHeroRepository(real_repository)

    print("\nПервый запрос:")
    first_result = proxy.find_by_name(hero.name)
    print("Найден герой:", first_result.name)

    print("\nВторой запрос:")
    second_result = proxy.find_by_name(hero.name)
    print("Найден герой:", second_result.name)

    print("\nРезультаты:")
    print("Обращения к реальному хранилищу:", real_repository.read_count)
    print("Попадания в кэш:", proxy.cache_hits)
    print("Промахи кэша:", proxy.cache_misses)

    print("Оба результата ссылаются на один объект:",
          first_result is second_result)

    print("\n9) FACADE")

    game = GameFacade()

    print("\nСоздание героя через фасад:")
    facade_hero = game.create_hero("Артур")
    print("Герой:", facade_hero.name)
    print("Класс:", facade_hero.hero_class.display_name)
    print("Здоровье:", facade_hero.health)

    print("\nСписок локаций:")
    for location in game.get_locations():
        print(
            f"- {location.display_name} "
            f"(рекомендуемый уровень: {location.recommended_level})"
        )

    print("\nПоиск локации через фасад:")
    forest = game.get_location("forest")
    print("Найдена локация:", forest.display_name)

    print("\nТовары торговца:")
    for item in game.merchant.showcase:
        print(f"- {item.name}: {item.price} золота")

    print("\n10) STRATEGY")

    enemy = Goblin()
    base_experience = enemy.experience_reward

    standard_strategy = StandardExperienceStrategy()
    double_strategy = DoubleExperienceStrategy()

    print("Базовый опыт:", base_experience)

    print(
        "Стандартная стратегия:",
        standard_strategy.calculate(base_experience)
    )

    print(
        "Стратегия двойного опыта:",
        double_strategy.calculate(base_experience)
    )

    forest = Forest(catalog)
    forest.set_experience_strategy(double_strategy)

    print("Стратегия установлена для локации: Мистический лес")

    print("\n11) OBSERVER")

    observer_hero = (
        HeroBuilder()
        .set_name("Артур")
        .set_hero_class(HeroClass.WARRIOR)
        .set_starter_kit(HeroClass.WARRIOR.get_starter_kit(catalog))
        .build()
    )

    console_observer = ConsoleObserver()
    achievement_observer = AchievementObserver()

    observer_hero.subscribe(console_observer)
    observer_hero.subscribe(achievement_observer)

    print("Подписаны два наблюдателя.")

    observer_hero.gain_experience(100)

    observer_hero.add_item(catalog.create(TRAINING_SWORD))

    print("\n12) CHAIN OF RESPONSIBILITY")

    validation_data = {
        "name": "Артур",
        "hero_class": HeroClass.WARRIOR,
        "starter_kit": HeroClass.WARRIOR.get_starter_kit(catalog)
    }

    name_handler = NameValidationHandler()
    class_handler = ClassValidationHandler()
    kit_handler = StarterKitValidationHandler()

    name_handler.set_next(class_handler).set_next(kit_handler)

    try:
        name_handler.handle(validation_data)
        print("Все проверки успешно пройдены.")

        validated_hero = (
            HeroBuilder()
            .set_name(validation_data["name"])
            .set_hero_class(validation_data["hero_class"])
            .set_starter_kit(validation_data["starter_kit"])
            .build()
        )

        print(f"Герой {validated_hero.name} успешно создан.")

    except ValueError as error:
        print(f"Ошибка проверки: {error}")

    print("\n========== END OF DEMO ==========\n")


if __name__ == "__main__":
    run_demo()
