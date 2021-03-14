from wsgiref.util import setup_testing_defaults
import urllib.parse
from time import time


def view_404_page(request):
    print(request)
    return '404 Not Found', b'404 Page not found'


class Application:
    def __init__(self, routes, fronts):
        self.routes = routes
        self.fronts = fronts

    def __call__(self, environ, start_response):
        setup_testing_defaults(environ)
        request_method = environ['REQUEST_METHOD']
        path = environ['PATH_INFO']
        request = {}

        if not path.endswith('/'):
            path = path + '/'

        if request_method == 'GET':
            request['method'] = 'GET'
            # print('GET запрос')
            data_str = environ['QUERY_STRING']
            # декодируем urlencoded в utf-8
            data_str = urllib.parse.unquote(data_str)
            data = self.pars_data(data_str)
            # if data:
            #     print(f'Сообщение от {data["email"]}\n'
            #           f'Тема: {data["theme"]}\n'
            #           f'Сообщение: {data["message"]}')
        elif request_method == 'POST':
            request['method'] = 'POST'
            # Получаем данные POST-запроса в виде байт строки
            data_bytes = self.get_wsgi_input_bytes(environ)
            # декодируем в str
            data_str = data_bytes.decode(encoding='utf-8')
            # декодируем urlencoded в utf-8
            data_str = urllib.parse.unquote(data_str)
            # преобразуем str в dict
            data = self.pars_data(data_str)

            # print(f'Сообщение от {data["email"]}\n'
            #       f'Тема: {data["theme"]}\n'
            #       f'Сообщение: {data["message"]}')
            # print(data)

        if path in self.routes:
            view = self.routes[path]
        else:
            view = view_404_page

        request.update(data)
        for front in self.fronts:
            front(request)

        response, page = view(request)
        start_response(response, [('Content-type', 'text/html')])
        return [page]

    @staticmethod
    def debug(func):
        '''Декоратор. Выводит название функции и время ее выполнения.
        Использовать перед декоратором add_route.'''

        def wrap(*args, **kwargs):
            start = time()
            result = func(*args, **kwargs)
            end = time()
            print(f'\nФункция {func.__name__} время выполнения: {end - start}\n')
            return result

        return wrap

    def add_route(self, url):
        '''Функция для передачи url в функцию decorator'''

        def decorator(view):
            '''Декоратор. Заменяет декорируюмую ф-цию на NoneType,
            но сохраняет её исходную форму в routes.'''
            self.routes[url] = view

        return decorator

    def get_wsgi_input_bytes(self, env):
        '''Получение данных POST запроса'''
        data = env['wsgi.input'].read()
        return data

    def pars_data(self, data: str):
        result = {}
        if data:
            data = data.split('&')
            for item in data:
                key, val = item.split('=')
                result[key] = val
        return result


class ApplicationLog(Application):
    def __call__(self, environ, start_response):
        print('\nЛогирующий режим:')
        print(environ)
        return super().__call__(environ, start_response)


class ApplicationFake(Application):
    def __call__(self, environ, start_response):
        start_response("200 OK", [('Content-type', 'text/html')])
        return b"Hello from Fake"
