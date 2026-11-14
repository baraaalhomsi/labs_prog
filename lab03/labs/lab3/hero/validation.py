from abc import ABC, abstractmethod
from .hero_class import HeroClass

class ValidationHandler(ABC):

    def __init__(self):
        self._next_handler = None

    def set_next(self, handler):
        self._next_handler = handler
        return handler

    def handle(self, data):
        self.validate(data)

        if self._next_handler:
            return self._next_handler.handle(data)

        return True

    @abstractmethod
    def validate(self, data):
        pass

class NameValidationHandler(ValidationHandler):

    def validate(self, data):
        name = data.get("name")

        if not isinstance(name, str) or not name.strip():
            raise ValueError("Имя героя не может быть пустым")

class ClassValidationHandler(ValidationHandler):

    def validate(self, data):
        hero_class = data.get("hero_class")

        if not isinstance(hero_class, HeroClass):
            raise ValueError("Необходимо выбрать класс героя")

class StarterKitValidationHandler(ValidationHandler):

    def validate(self, data):
        if data.get("starter_kit") is None:
            raise ValueError("Стартовый набор не выбран")