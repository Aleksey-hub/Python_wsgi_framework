class Singleton(type):
    def __init__(cls, name, bases, attrs):
        super().__init__(name, bases, attrs)
        cls.__instance = {}

    def __call__(cls, *args, **kwargs):
        if args:
            name_logger = args[0]
        elif kwargs:
            name_logger = kwargs['name_logger']
        else:
            raise TypeError('Необходимо ввести имя логгера.')

        if name_logger not in cls.__instance:
            cls.__instance[name_logger] = super().__call__(*args, **kwargs)
        return cls.__instance[name_logger]