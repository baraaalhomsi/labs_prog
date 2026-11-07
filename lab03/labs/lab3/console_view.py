from .combat.models import EventType, Side, Outcome


class ConsoleView:
    def describe(self, item):
        if item is None:
            return "Ничего"
        enchantments = ", ".join(e.code for e in item.enchantments)
        suffix = f" [{enchantments}]" if enchantments else ""
        return f"{item.name}{suffix} ({item.description})"

    def print_hero(self, hero):
        print(
            f"{hero.name}, {hero.hero_class.display_name} {hero.level} ур. | "
            f"здоровье {hero.health}/{hero.max_health} | опыт "
            f"{hero.experience}/{hero.experience_to_next_level} | золото {hero.gold}"
        )
        print("  Снаряжение:", self.describe(hero.weapon), "|", self.describe(hero.armor))
        print(f"  Предметов в инвентаре: {len(hero.inventory)}")

    def print_report(self, report, location_name):
        battle = report.battle
        print(f"\n=== {location_name} (сид {report.seed}) ===")
        print(f"{battle.hero.name} встречает {battle.enemy.name} ({battle.enemy.max_health} здоровья)")
        for event in battle.events:
            source = battle.hero if event.source == Side.HERO else battle.enemy
            target = battle.hero if event.target == Side.HERO else battle.enemy
            if event.type == EventType.DEATH:
                print(f"{target.name} повержен!")
            else:
                prefix = "КРИТ! " if event.type == EventType.CRITICAL_HIT else ""
                print(
                    f"[раунд {event.round}] {source.name} -> {target.name}: "
                    f"{prefix}{event.amount} урона, осталось {event.target_health_after}"
                )
        rewards = report.rewards
        if battle.outcome == Outcome.VICTORY:
            print(f"Победа! +{rewards.experience} опыта, +{rewards.gold} золота")
            if rewards.loot:
                print("Добыча:", self.describe(rewards.loot))
            if rewards.levels_gained:
                print(f"Новый уровень! Получено уровней: {rewards.levels_gained}")
        else:
            print(f"Поражение. Герой теряет {abs(rewards.gold)} золота.")

    def print_inventory(self, hero):
        if not hero.inventory:
            print("Инвентарь пуст.")
            return
        for index, item in enumerate(hero.inventory, 1):
            print(f"{index}. {self.describe(item)} — {item.price} золота")
