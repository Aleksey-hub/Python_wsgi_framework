from fwsgi.fwsgi import Aplication
from fwsgi.templator import render
from logger import Logger

logger = Logger('main')

def index(request):
    logger.log('Загрузка главной страницы')
    # print(request)
    # return '200 OK', [b'index']
    response = render('index.html', title='Главная страница')
    return '200 OK', response.encode()


def contacts(request):
    logger.log('Загрузка страницы контактов')
    # print(request)
    # return '200 OK', [b'about']
    response = render('contacts.html', title='Контакты')
    return '200 OK', response.encode()


routes = {
    '/': index,
    '/contacts/': contacts
}


def secret_front(request):
    request['secret'] = 'secret'


fronts = [secret_front]

application = Aplication(routes, fronts)
