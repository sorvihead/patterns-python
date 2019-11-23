from abc import ABC, abstractmethod


class Engine:
    pass


class ObservableEngine(Engine):
    def __init__(self):
        self.__subscribers = set()

    def subscribe(self, subscriber):
        self.__subscribers.add(subscriber)

    def unsubscribe(self, subscriber):
        if subscriber in self.__subscribers:
            self.__subscribers.remove(subscriber)

    def notify(self, achievement):
        for subscriber in self.__subscribers:
            subscriber.update(achievement)


class AbstractObserver(ABC):
    @abstractmethod
    def update(self, achievement):
        pass


class ShortNotificationPrinter(AbstractObserver):
    def __init__(self):
        self.achievements = set()

    def update(self, achievement):
        self.achievements.add(achievement['title'])
        print(f"Achievement recieved: {achievement['title']}")


class FullNotificationPrinter(AbstractObserver):
    def __init__(self):
        self.achievements = list()

    def update(self, achievement):
        if achievement not in self.achievements:
            self.achievements.append(achievement)
        print(f"Achievement recieved: {achievement}")


if __name__ == '__main__':
    notifier = ShortNotificationPrinter()
    notifier2 = FullNotificationPrinter()
    manager = ObservableEngine()
    manager.subscribe(notifier)
    manager.subscribe(notifier2)
    manager.notify({"title": "Покоритель", "text": "Дается при выполнении всех заданий в игре"})
    manager.notify({"title": "Лох", "text": "Не может написать наблюдателя"})
