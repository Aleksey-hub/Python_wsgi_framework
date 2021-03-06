from fwsgi.fwsgi import Application, ApplicationFake, ApplicationLog
from fwsgi.templator import render
from logger import Logger
from models import Website, Category

logger = Logger('main')
site = Website()
#
categories1 = site.add_categories('Python')
site.add_courses('Python для профессионалов', categories1)
site.add_courses('Python для начинающих', categories1)
categories1 = site.add_categories('Java')

routes = {
    # '/': index,
    # '/contacts/': contacts,
    # '/new_course/': new_course,
    # '/new_category/': new_category
}


def secret_front(request):
    request['secret'] = 'secret'


fronts = [secret_front]

application = Application(routes, fronts)
# application = ApplicationFake(routes, fronts)
# application = ApplicationLog(routes, fronts)


@application.add_route('/')
@application.debug
def index(request):
    logger.log('Загрузка главной страницы')
    # print(request)
    # return '200 OK', [b'index']
    response = render('index.html', routes=routes, title='Главная страница', site=site)
    return '200 OK', response.encode()


@application.add_route('/contacts/')
@application.debug
def contacts(request):
    logger.log('Загрузка страницы контактов')
    # print(request)
    # return '200 OK', [b'about']
    response = render('contacts.html', routes=routes, title='Контакты')
    return '200 OK', response.encode()


@application.add_route('/new_course/')
def new_course(request):
    title = 'Создание нового курса'
    logger.log(title)
    # переменные для копирования уже существующего курса:
    name_copy = ''
    category_copy = ''
    if request['method'] == 'POST':
        category = site.get_category_by_name(request['category'])
        site.add_courses(request['course_name'], category)
    # копирование уже существующего курса:
    if request['method'] == 'GET' and 'name_copy' in request and 'category_copy' in request:
        name_copy = request['name_copy']
        category_copy = site.get_category_by_name(request['category_copy'])
    # print(request)
    response = render('new_course.html', routes=routes, title=title, site=site, name_copy=name_copy,
                      category_copy=category_copy)
    return '200 OK', response.encode()


@application.add_route('/new_category/')
def new_category(request):
    title = 'Создание новой категории'
    logger.log(title)
    if request['method'] == 'POST':
        site.add_categories(request['category'])
    response = render('new_category.html', routes=routes, title=title, site=site)
    return '200 OK', response.encode()