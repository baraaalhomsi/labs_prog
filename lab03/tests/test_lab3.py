import unittest

from labs.lab3.core.dice import Dice
from labs.lab3.hero.builder import HeroBuilder
from labs.lab3.hero.hero_class import HeroClass
from labs.lab3.items.catalog import create_default_catalog, TRAINING_SWORD, IRON_SWORD
from labs.lab3.items.enchantment import SHARP
from labs.lab3.kits.factories import WarriorKitFactory, RangerKitFactory
from labs.lab3.world.locations import Forest, Crypt
from labs.lab3.camp.merchant import Merchant


class Lab3Tests(unittest.TestCase):
    def setUp(self):
        self.catalog = create_default_catalog()
        self.hero = (
            HeroBuilder().set_name("Тест").set_hero_class(HeroClass.WARRIOR)
            .set_starter_kit(HeroClass.WARRIOR.get_starter_kit(self.catalog)).build()
        )

    def test_singleton(self):
        self.assertIs(Dice(), Dice())

    def test_builder_creates_hero(self):
        self.assertEqual(self.hero.max_health, 120)
        self.assertEqual(self.hero.gold, 50)

    def test_abstract_factories_create_different_families(self):
        warrior = WarriorKitFactory(self.catalog)
        ranger = RangerKitFactory(self.catalog)
        self.assertNotEqual(warrior.create_weapon().code, ranger.create_weapon().code)
        self.assertNotEqual(warrior.create_armor().code, ranger.create_armor().code)

    def test_factory_method_returns_different_enemy_types(self):
        self.assertNotEqual(Forest(self.catalog)._create_enemy().code,
                            Crypt(self.catalog)._create_enemy().code)

    def test_prototype_copy_is_independent(self):
        original = self.catalog.create(TRAINING_SWORD)
        clone = original.copy()
        clone.enchant(SHARP)
        self.assertEqual(original.price, 20)
        self.assertEqual(clone.price, 40)
        self.assertEqual(len(original.enchantments), 0)

    def test_merchant_buy_and_sell(self):
        merchant = Merchant(self.catalog, [IRON_SWORD])
        item = merchant.buy(self.hero, IRON_SWORD)
        self.assertEqual(self.hero.gold, 50 - item.price)
        self.assertIn(item, self.hero.inventory)
        earned = merchant.sell(self.hero, item)
        self.assertEqual(earned, item.price // 2)
        self.assertNotIn(item, self.hero.inventory)


if __name__ == "__main__":
    unittest.main()
