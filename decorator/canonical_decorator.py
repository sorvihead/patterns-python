from abc import ABC, abstractmethod


class Creature(ABC):
    """
    Абстрактный базовый класс животного
    """

    @abstractmethod
    def feed(self):
        pass

    @abstractmethod
    def move(self):
        pass

    @abstractmethod
    def make_noise(self):
        pass


class Animal(Creature):

    def feed(self):
        print("I eat grass")

    def move(self):
        print("I walk forward")

    def make_noise(self):
        print("WOO!")


class AbstractDecorator(Creature):
    """
    Абстрактный декоратор. Принимает экземпляр класса, который нужно проапгрейдить
    """

    def __init__(self, base):
        self.base = base

    def move(self):
        self.base.move()

    def feed(self):
        self.base.feed()

    def make_noise(self):
        self.base.make_noise()


class Swimming(AbstractDecorator):
    """
    Здесь и ниже, пример декораторов, которые изменяют поведение различных методов
    """

    def move(self):
        print("I swim forward")

    def make_noise(self):
        print("...")


class Predator(AbstractDecorator):

    def feed(self):
        print("I eat other animals")


class Fast(AbstractDecorator):

    def move(self):
        self.base.move()
        print("Fast!")


if __name__ == '__main__':
    # Обычное животное, к которому не применен декоратор
    animal = Animal()
    animal.move()
    animal.feed()
    animal.make_noise()

    # Применение декоратора Swimming к животному
    swimming = Swimming(animal)
    swimming.move()
    swimming.make_noise()
    swimming.feed()

    # Наложение декоратора Predator на декоратор Swimming
    predator = Predator(swimming)
    predator.feed()
    predator.make_noise()
    predator.move()

    # Наложение декоратора Fast на декоратор Predator
    fast = Fast(predator)
    fast.make_noise()
    fast.feed()
    fast.move()

    # Наложение декоратора Fast на декоратор Fast
    faster = Fast(fast)
    faster.make_noise()
    faster.feed()
    faster.move()

    # Удаление декоратора Predator
    faster.base.base = faster.base.base.base
    faster.make_noise()
    faster.feed()
    faster.move()
