import abc


class Observer(metaclass=abc.ABCMeta):

    @abc.abstractmethod
    def update(self, arg):
        pass


class Subject:
    def __init__(self):
        self.observers = []

    def attach(self, observer):
        observer._subject = self
        self.observers.append(observer)

    def detach(self, observer):
        observer._subject = None
        self.observers.remove(observer)

    def notify(self):
        for observer in self.observers:
            observer.update(self)
