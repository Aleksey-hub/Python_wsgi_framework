class Singleton(type):
    def __init__(cls, name, bases, attrs):
        super().__init__(name, bases, attrs)
        cls.__instance = {}

    def __call__(cls, name_logger):
        if name_logger not in cls.__instance:
            cls.__instance[name_logger] = super().__call__()
        return cls.__instance[name_logger]