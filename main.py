from wsgiref.simple_server import make_server
from fwsgi.fwsgi import Application, ApplicationFake, ApplicationLog
from fwsgi.templator import render
from logger import Logger
from models import Website, Category, UsersCreator, Student

logger = Logger('main')
site = Website()
#
categories1 = site.add_categories('Python')
course1 = site.add_courses('Python для профессионалов', categories1)
course2 = site.add_courses('Python для начинающих', categories1)
categories1 = site.add_categories('Java')

student1 = site.add_user('student', 'Иван', 'Иванов')
teacher1 = site.add_user('teacher', 'Дмитрий', 'Иванов')

course1.add_user(student1)
course1.add_user(teacher1)

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


@application.add_route('/add_student/')
def add_student(request):
    title = 'Запись студентов на курс'
    logger.log(title)

    students = []
    for student in site.users:
        if isinstance(student, Student):
            students.append(student)

    if request['method'] == 'POST':
        name, last_name = request['student'].split('+')
        student = site.get_student_by_name(name, last_name)

        course_name = request['course'].replace('+', ' ')
        course = site.get_course_by_name(course_name)

        course.add_user(student)
        # print(course.users)

    response = render('add_student.html', routes=routes, title=title, courses=site.courses, students=students)
    return '200 OK', response.encode()


@application.add_route('/list_student/')
def list_student(request):
    title = 'Список студентов'
    logger.log(title)

    students = []
    for student in site.users:
        if isinstance(student, Student):
            students.append(student)

    response = render('list_student.html', routes=routes, title=title, students=students)
    return '200 OK', response.encode()


@application.add_route('/new_user/')
def new_user(request):
    title = 'Создание нового пользователя'
    logger.log(title)

    if request['method'] == 'POST':
        site.add_user(request['user_type'], request['name'], request['last_name'])

    response = render('new_user.html', routes=routes, title=title, site=site, user_types=UsersCreator.user_types)
    return '200 OK', response.encode()


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
        new_course = site.add_courses(request['course_name'], category)

    # print(request)
    response = render('new_course.html', routes=routes, title=title, site=site, name_copy=name_copy,
                      category_copy=category_copy)
    return '200 OK', response.encode()


@application.add_route('/copy_course/')
def copy_course(request):
    title = 'Главная страница'
    logger.log(title)

    # копирование уже существующего курса:
    copy_course = site.get_course_by_name(request['name_copy'])
    print(copy_course)

    new_course = copy_course.clone()

    name_copy = 'new ' + request['name_copy']
    new_course.course_name = name_copy

    category = site.get_category_by_name(request['category_copy'])
    new_course.category = category

    # site.add_courses(new_course, category)
    site.courses.append(new_course)

    response = render('index.html', routes=routes, title=title, site=site)
    return '200 OK', response.encode()


@application.add_route('/edit_course/')
def edit_course(request):
    title = 'Изменение курса'
    logger.log(title)

    new_category = ''
    course_name = ''
    category = ''
    # print(request)

    if request['method'] == 'POST':
        new_course_name = request['new_course_name'].replace('+', ' ')
        old_course_name = request['old_course_name'].replace('+', ' ')
        course = site.get_course_by_name(old_course_name)
        print(course.observers)
        course.notify()
        course.course_name = new_course_name

        new_category_course = site.get_category_by_name(request['category'])
        course.category = new_category_course

        response = render('index.html', routes=routes, title=title, site=site)
    # копирование данных выбранного для изменения курса:
    if request['method'] == 'GET' and 'course_name' in request and 'category' in request:
        print(request)
        course_name = request['course_name']
        category = site.get_category_by_name(request['category'])
        # print(request)
        response = render('edit_course.html', routes=routes, title=title, site=site, course_name=course_name,
                          category=category, new_category=new_category)
    return '200 OK', response.encode()


@application.add_route('/new_category/')
def new_category(request):
    title = 'Создание новой категории'
    logger.log(title)
    if request['method'] == 'POST':
        site.add_categories(request['category'])
    response = render('new_category.html', routes=routes, title=title, site=site)
    return '200 OK', response.encode()

# with make_server('', 8000, application) as httpd:
#     print("Serving on port 8000...")
#     httpd.serve_forever()
