from .camp.merchant import Merchant
from .combat.models import Outcome
from .console_view import ConsoleView
from .core.dice import Dice
from .hero.builder import HeroBuilder
from .hero.hero_class import HeroClass
from .items.catalog import (
    create_default_catalog, IRON_SWORD, ELVEN_BOW, EMBER_STAFF,
    CHAINMAIL, PLATE_ARMOR
)
from .world.locations import Forest, Crypt, DragonLair
from .world.registry import LocationRegistry
from .demo import run_demo

VIEW = ConsoleView()


def read_choice(count):
    try:
        choice = int(input("> ").strip())
        if 1 <= choice <= count:
            return choice - 1
    except ValueError:
        pass
    return -1


def create_hero(catalog):
    print("\nСоздайте своего героя!")
    classes = list(HeroClass)
    for index, hero_class in enumerate(classes, 1):
        kit = hero_class.get_starter_kit(catalog)
        print(
            f"{index}. {hero_class.display_name} (здоровье {hero_class.base_health}): "
            f"{VIEW.describe(kit.create_weapon())}, {VIEW.describe(kit.create_armor())}"
        )
    selected = read_choice(len(classes))
    if selected < 0:
        selected = 0
    hero_class = classes[selected]
    while True:
        name = input("Введите имя героя: ").strip()
        try:
            return (
                HeroBuilder()
                .set_name(name)
                .set_hero_class(hero_class)
                .set_starter_kit(hero_class.get_starter_kit(catalog))
                .build()
            )
        except ValueError as error:
            print("Не получилось создать героя:", error)


def go_on_expedition(hero, locations):
    all_locations = locations.get_all()
    print("\nКуда отправимся?")
    for index, location in enumerate(all_locations, 1):
        print(f"{index}. {location.display_name} (рекомендуемый уровень {location.recommended_level})")
    index = read_choice(len(all_locations))
    if index < 0:
        return
    location = all_locations[index]
    report = location.explore(hero, Dice().next_seed())
    VIEW.print_report(report, location.display_name)
    if report.battle.outcome == Outcome.VICTORY and location.code == "dragon-lair":
        print(f"\nДракон повержен! Барды будут помнить героя {hero.name}!")


def manage_equipment(hero):
    inventory = hero.inventory
    if not inventory:
        print("Инвентарь пуст.")
        return
    VIEW.print_inventory(hero)
    index = read_choice(len(inventory))
    if index < 0:
        return
    item = inventory[index]
    try:
        hero.equip(item)
        print("Экипировано:", VIEW.describe(item))
    except ValueError as error:
        print(error)


def visit_merchant(hero, merchant):
    print(f'\nТорговец: "Чего желаешь?" (золото: {hero.gold})')
    print("1. Купить  2. Продать  0. Назад")
    choice = input("> ").strip()
    if choice == "1":
        showcase = merchant.showcase
        for index, item in enumerate(showcase, 1):
            print(f"{index}. {VIEW.describe(item)} — {item.price} золота")
        index = read_choice(len(showcase))
        if index >= 0:
            try:
                bought = merchant.buy(hero, showcase[index].code)
                print("Куплено:", VIEW.describe(bought))
            except ValueError as error:
                print(error)
    elif choice == "2":
        inventory = hero.inventory
        if not inventory:
            print("Продавать нечего (экипированные предметы продать нельзя).")
            return
        VIEW.print_inventory(hero)
        index = read_choice(len(inventory))
        if index >= 0:
            item = inventory[index]
            price = merchant.sell(hero, item)
            print(f"Продано: {item.name} за {price} золота.")


def main():
    catalog = create_default_catalog()
    locations = LocationRegistry([
        Forest(catalog), Crypt(catalog), DragonLair(catalog)
    ])
    merchant = Merchant(catalog, [
        IRON_SWORD, ELVEN_BOW, EMBER_STAFF, CHAINMAIL, PLATE_ARMOR
    ])
    hero = create_hero(catalog)
    print(f"\n{hero.name} разбивает лагерь на опушке мистического леса.")

    while True:
        print()
        VIEW.print_hero(hero)
        print("\n1. Экспедиция  2. Снаряжение  3. Торговец  4. Demo паттернов  0. Выход")
        choice = input("> ").strip()
        if choice == "1":
            go_on_expedition(hero, locations)
        elif choice == "2":
            manage_equipment(hero)
        elif choice == "3":
            visit_merchant(hero, merchant)
        elif choice == "4":
            run_demo()
        elif choice == "0":
            print("До свидания!")
            break
        else:
            print("Такого варианта нет.")


if __name__ == "__main__":
    main()
