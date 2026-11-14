from abc import ABC, abstractmethod

class ExperienceStrategy(ABC):

    @abstractmethod
    def calculate(self, base_experience: int) -> int:
        pass

class StandardExperienceStrategy(ExperienceStrategy):

    def calculate(self, base_experience: int) -> int:
        return base_experience

class DoubleExperienceStrategy(ExperienceStrategy):

    def calculate(self, base_experience: int) -> int:
        return base_experience * 2