from abc import ABC, abstractmethod


class NotificationManager:
    def __init__(self):
        self.__subscribers = set()

    def subscribe(self, subscriber):
        self.__subscribers.add(subscriber)

    def unsubscribe(self, subscriber):
        self.__subscribers.remove(subscriber)

    def notify(self, message):
        for subscriber in self.__subscribers:
            subscriber.update(message)


class AbstractObserver(ABC):
    @abstractmethod
    def update(self, message):
        pass


class MessageNotifier(AbstractObserver):
    def __init__(self, name):
        self.__name = name

    def update(self, message):
        print(f"{self.__name} recieved message!")


class MessagePrinter(AbstractObserver):
    def __init__(self, name):
        self.__name = name
        
    def update(self, message):
        print(f"{self.__name} recieved message: {message}")


if __name__ == '__main__':
    n = MessageNotifier("Notifier1")
    p1 = MessagePrinter("Printer1")
    p2 = MessagePrinter("Printer2")

    manager = NotificationManager()

    manager.subscribe(n)
    manager.subscribe(p1)
    manager.subscribe(p2)

    manager.notify("Hi")