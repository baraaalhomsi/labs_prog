from .events import Observer, Event

class ConsoleObserver(Observer):

    def update(self, event: Event):
        if event.event_type == "level_up":
            print(
                f"[Уведомление] {event.data['name']} "
                f"получил новый уровень: {event.data['level']}"
            )

        elif event.event_type == "item_added":
            print(
                f"[Уведомление] Новый предмет добавлен: "
                f"{event.data['item']}"
            )

class AchievementObserver(Observer):

    def update(self, event: Event):
        if event.event_type == "level_up":
            if event.data["level"] >= 2:
                print(
                    f"[Достижение] {event.data['name']} "
                    f"достиг второго уровня!"
                )