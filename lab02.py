from abc import ABC, abstractmethod
class Pet(ABC):
    @abstractmethod
    def express(self) -> None:
        ...
    @abstractmethod
    def get_name(self) -> str:
        ...
    @abstractmethod
    def get_age(self) -> int:
        ...
    @abstractmethod
    def get_age_in_human_years(self) -> int:
        ... 

class Animal(Pet):
    def __init__(self, name: str, age: int):
        self.__name = name
        self.__age = age
    def happy_birthday(self) -> None: 
        self.__age += 1
    def get_name(self) -> str:
        return self.__name
    def get_age(self) -> int:
        return self.__age

class Turtle(Animal):
    def get_age_in_human_years(self) -> int:
        if self.get_age() <= 0:
            return 0
        else:
            return 15 + (self.get_age() - 1) * 2
    def express(self) -> None:
        print("""
                  _____     ____
                 /      \\  |  o |
                |        |/ ___\\|
                |_________/
                |_|_| |_|_|
                """)

class Parrot(Animal):
    def get_age_in_human_years(self) -> int:
        if self.get_age() <= 0:
            return 0
        else:
            return self.get_age() * 5
    def express(self) -> None:
            print(f'{self.get_name()}: "Hello!"')
            print("""
                     \\
                     (o>
                  \\\\_//)
                   \\_/_)
                    _|_
                    """)

class Person:
    def __init__(self, name: str, pet: Pet | None = None):
        self.__name = name
        self.__pet = pet
    def set_pet(self, pet: Pet | None) -> None:
        self.__pet = pet
    def get_pet_info(self) -> None:
        print("--------------------")
        if self.__pet is None:
            print(f'{self.__name} has no pet yet')
        else:
            print(f'Pet for {self.__name} is named {self.__pet.get_name()}')
            print(f'Age: {self.__pet.get_age()} year(s), about {self.__pet.get_age_in_human_years()} human years')
            print("And it expresses itself like this:")
            self.__pet.express()
        print("--------------------")

if __name__ == "__main__":
    kesha = Parrot("Kesha", 2)
    zavala = Turtle("Zavala", 4)
    kesha.happy_birthday()

    jack = Person("Jack", kesha)
    john = Person("John")

    jack.get_pet_info()
    john.get_pet_info()

    john.set_pet(zavala)
    john.get_pet_info()
    