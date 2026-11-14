from abc import ABC, abstractmethod
from dataclasses import dataclass

@dataclass(frozen=True)
class Event:
    event_type: str
    data: dict

class Observer(ABC):

    @abstractmethod
    def update(self, event: Event):
        pass

class EventManager:

    def __init__(self):
        self._observers = []

    def subscribe(self, observer: Observer):
        if observer not in self._observers:
            self._observers.append(observer)

    def unsubscribe(self, observer: Observer):
        if observer in self._observers:
            self._observers.remove(observer)

    def notify(self, event: Event):
        for observer in tuple(self._observers):
            observer.update(event)