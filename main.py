from fwsgi.fwsgi import Aplication
from fwsgi.templator import render


def index(request):
    print(request)
    # return '200 OK', [b'index']
    response = render('templates/index.html')
    return '200 OK', response.encode()


def contacts(request):
    print(request)
    # return '200 OK', [b'about']
    response = render('templates/contacts.html')
    return '200 OK', response.encode()


routes = {
    '/': index,
    '/contacts/': contacts
}


def secret_front(request):
    request['secret'] = 'secret'


fronts = [secret_front]

application = Aplication(routes, fronts)
