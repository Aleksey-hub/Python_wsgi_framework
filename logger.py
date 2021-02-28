from reusepatterns.singleton import Singleton


class Logger(metaclass=Singleton):
    def __init__(self, name):
        self.name = name

    def log(self, message):
        with open(f'{self.name}.log', 'w') as f:
            f.write(message)