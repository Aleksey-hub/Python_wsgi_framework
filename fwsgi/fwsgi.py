def index(request):
    print(request)
    return '200 OK', [b'index']


def about(request):
    print(request)
    return '200 OK', [b'about']


def view_404_page(request):
    print(request)
    return '404 Not Found', [b'404 Page not found']


routes = {
    '/': index,
    '/about/': about
}

def secret_front(request):
    request['secret'] = 'secret'


fronts = [secret_front]

class Aplication:
    def __init__(self, routes, fronts):
        self.routes = routes
        self.fronts = fronts

    def __call__(self, environ, start_response):
        path = environ['PATH_INFO']
        if not path.endswith('/'):
            path = path + '/'

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


application = Aplication(routes, fronts)
