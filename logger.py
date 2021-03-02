from datetime import datetime

from reusepatterns.singleton import Singleton


class Logger(metaclass=Singleton):
    def __init__(self, name):
        self.name = name

    def log(self, message):
        with open(f'{self.name}.log', 'a') as f:
            f.write(str(datetime.now()) + '\t' + message + '\n')