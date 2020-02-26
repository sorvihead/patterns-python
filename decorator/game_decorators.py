from abc import ABC, abstractmethod


class Hero:
    def __init__(self):
        self.positive_effects = []
        self.negative_effects = []
        self.stats = {
            "HP": 128,  # health points
            "MP": 42,  # magic points,
            "SP": 100,  # skill points
            "Strength": 15,  # сила
            "Perception": 4,  # восприятие
            "Endurance": 8,  # выносливость
            "Charisma": 2,  # харизма
            "Intelligence": 3,  # интеллект
            "Agility": 8,  # ловкость
            "Luck": 1  # удача
        }

    def get_positive_effects(self):
        return self.positive_effects.copy()

    def get_negative_effects(self):
        return self.negative_effects.copy()

    def get_stats(self):
        return self.stats.copy()


class AbstractEffect(Hero, ABC):

    def __init__(self, base: Hero):
        super(AbstractEffect, self).__init__()
        self.base = base

    @abstractmethod
    def get_negative_effects(self):
        pass

    @abstractmethod
    def get_positive_effects(self):
        pass

    @abstractmethod
    def get_stats(self):
        pass


class AbstractPositive(AbstractEffect, ABC):

    @abstractmethod
    def get_positive_effects(self):
        pass

    def get_negative_effects(self):
        return self.base.get_negative_effects()


class AbstractNegative(AbstractEffect, ABC):

    @abstractmethod
    def get_negative_effects(self):
        pass

    def get_positive_effects(self):
        return self.base.get_positive_effects()


class Berserk(AbstractPositive):

    def get_stats(self):
        stats = self.base.get_stats()
        stats["HP"] += 50
        stats["Strength"] += 7
        stats["Endurance"] += 7
        stats["Agility"] += 7
        stats["Luck"] += 7
        stats["Perception"] -= 3
        stats["Charisma"] -= 3
        stats["Intelligence"] -= 3
        return stats

    def get_positive_effects(self):
        positive_effects = self.base.get_positive_effects()
        positive_effects.append("Berserk")
        return positive_effects


class Blessing(AbstractPositive):

    def get_stats(self):
        stats = self.base.get_stats()
        stats["Strength"] += 2
        stats["Endurance"] += 2
        stats["Agility"] += 2
        stats["Luck"] += 2
        stats["Perception"] += 2
        stats["Charisma"] += 2
        stats["Intelligence"] += 2
        return stats

    def get_positive_effects(self):
        positive_effects = self.base.get_positive_effects()
        positive_effects.append("Blessing")
        return positive_effects


class Weakness(AbstractNegative):

    def get_stats(self):
        stats = self.base.get_stats()
        stats["Strength"] -= 4
        stats["Endurance"] -= 4
        stats["Agility"] -= 4
        return stats

    def get_negative_effects(self):
        negative_effects = self.base.get_negative_effects()
        negative_effects.append("Weakness")
        return negative_effects


class Curse(AbstractNegative):
    def get_stats(self):
        stats = self.base.get_stats()
        stats["Strength"] -= 2
        stats["Endurance"] -= 2
        stats["Agility"] -= 2
        stats["Luck"] -= 2
        stats["Perception"] -= 2
        stats["Charisma"] -= 2
        stats["Intelligence"] -= 2
        return stats

    def get_negative_effects(self):
        negative_effects = self.base.get_negative_effects()
        negative_effects.append("Curse")
        return negative_effects


class EvilEye(AbstractNegative):
    def get_stats(self):
        stats = self.base.get_stats()
        stats["Luck"] -= 10
        return stats

    def get_negative_effects(self):
        negative_effects = self.base.get_negative_effects()
        negative_effects.append("EvilEye")
        return negative_effects


if __name__ == '__main__':
    h = Hero()
    print(h.get_stats())
    print(h.get_negative_effects())
    print(h.get_positive_effects())

    b = Berserk(h)
    print(b.get_stats())
    print(b.get_positive_effects())
    print(b.get_negative_effects())

    print(b.base.get_stats())
    print(b.base.get_positive_effects())
    print(b.base.get_negative_effects())

    b2 = Berserk(b)

    print(b2.get_stats())
    print(b2.get_positive_effects())
    print(b2.get_negative_effects())

    bles = Blessing(b2)
    print(bles.get_stats())
    print(bles.get_positive_effects())
    print(bles.get_negative_effects())

    curse = Curse(bles)
    print(curse.get_stats())
    print(curse.get_positive_effects())
    print(curse.get_negative_effects())

    curse.base.base = curse.base.base.base
    print(curse.get_stats())
    print(curse.get_positive_effects())
    print(curse.get_negative_effects())
