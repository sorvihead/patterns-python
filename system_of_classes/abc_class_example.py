from abc import ABC, abstractmethod


class A(ABC):
    @abstractmethod
    def do_something(self):
        print('Hi!')


class B(A):
    def do_something(self):
        print("Hi2!")

    def do_something_else(self):
        print("Hello")
