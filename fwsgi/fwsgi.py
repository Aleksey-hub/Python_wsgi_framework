def view_404_page(request):
    print(request)
    return '404 Not Found', [b'404 Page not found']


class Aplication:
    def __init__(self, routes, fronts):
        self.routes = routes
        self.fronts = fronts

    def __call__(self, environ, start_response):
        request_method = environ['REQUEST_METHOD']
        path = environ['PATH_INFO']

        if not path.endswith('/'):
            path = path + '/'

        if request_method == 'GET':
            print('GET запрос')
            data_str = environ['QUERY_STRING']
            data = self.pars_data(data_str)
            print(f'Сообщение от {data["email"]}\n'
                  f'Тема: {data["theme"]}\n'
                  f'Сообщение: {data["message"]}')
        elif request_method == 'POST':
            print('POST запрос')
            # Получаем данные POST-запроса в виде байт строки
            data_bytes = self.get_wsgi_input_bytes(environ)
            # декодируем в str
            data_str = data_bytes.decode(encoding='utf-8')
            # преобразуем str в dict
            data = self.pars_data(data_str)

            print(f'Сообщение от {data["email"]}\n'
                  f'Тема: {data["theme"]}\n'
                  f'Сообщение: {data["message"]}')

        if path in self.routes:
            view = self.routes[path]
        else:
            view = view_404_page

        request = {}
        for front in self.fronts:
            front(request)

        response, page = view(request)
        start_response(response, [('Content-type', 'text/html')])
        return page


    def get_wsgi_input_bytes(self, env):
        '''Получение данных POST запроса'''
        data = env['wsgi.input'].read()
        return data

    def pars_data(self, data:str):
        result = {}
        data = data.split('&')
        for item in data:
            key, val = item.split('=')
            result[key] = val
        return result
