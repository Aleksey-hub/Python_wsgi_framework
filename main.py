from wsgiref.simple_server import make_server
from fwsgi.fwsgi import Application, ApplicationFake, ApplicationLog
from fwsgi.templator import render
from logger import Logger
from mappers import MapperRegistry
from models import Website, Category, UsersCreator, Student, CoursesStudents, Course
from orm.unitofwork import UnitOfWork

logger = Logger('main')
site = Website()
UnitOfWork.new_current()
UnitOfWork.get_current().set_mapper_registry(MapperRegistry)
#
# categories1 = site.add_categories('Python')
# course1 = site.add_courses('Python для профессионалов', categories1)
# course2 = site.add_courses('Python для начинающих', categories1)
# categories2 = site.add_categories('Java')

# student1 = site.add_user('student', 'Иван', 'Иванов')
# teacher1 = site.add_user('teacher', 'Дмитрий', 'Иванов')

# course1.add_user(student1)
# course1.add_user(teacher1)

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

    # students = []
    # for student in site.users:
    #     if isinstance(student, Student):
    #         students.append(student)
    mapper = MapperRegistry.get_current_mapper('student')
    students = mapper.find_all()

    mapper = MapperRegistry.get_current_mapper('course')
    courses = mapper.find_all()

    if request['method'] == 'POST':
        student_id = request['student']
        course_id = request['course']

        course_student = CoursesStudents(course_id, student_id)
        mapper = MapperRegistry.get_current_mapper('courses_students')
        mapper.insert(course_student)

    response = render('add_student.html', routes=routes, title=title, courses=courses, students=students)
    return '200 OK', response.encode()


@application.add_route('/list_student/')
def list_student(request):
    title = 'Список студентов'
    logger.log(title)

    # students = []
    # for student in site.students:
    #     if isinstance(student, Student):
    #         students.append(student)

    mapper = MapperRegistry.get_current_mapper('student')
    students = mapper.find_all()

    response = render('list_student.html', routes=routes, title=title, students=students)
    return '200 OK', response.encode()


@application.add_route('/new_user/')
def new_user(request):
    title = 'Создание нового пользователя'
    logger.log(title)

    if request['method'] == 'POST':
        # site.add_user(request['user_type'], request['first_name'], request['last_name'])
        student = Student(request['first_name'], request['last_name'])
        mapper = MapperRegistry.get_current_mapper('student')
        mapper.insert(student)

    response = render('new_user.html', routes=routes, title=title, site=site, user_types=UsersCreator.user_types)
    return '200 OK', response.encode()


@application.add_route('/')
@application.debug
def index(request):
    logger.log('Загрузка главной страницы')
    # print(request)
    # return '200 OK', [b'index']
    mapper_course = MapperRegistry.get_current_mapper('course')
    courses = mapper_course.find_all()

    mapper_category = MapperRegistry.get_current_mapper('category')
    categories = mapper_category.find_all()

    response = render('index.html', routes=routes, title='Главная страница', courses=courses, categories=categories)
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
    mapper_categories = MapperRegistry.get_current_mapper('category')
    categories = mapper_categories.find_all()
    # переменные для копирования уже существующего курса:
    name_copy = ''
    category_copy = ''
    if request['method'] == 'POST':
        mapper_course = MapperRegistry.get_current_mapper('course')
        course = Course(request['course_name'], request['category'])
        # category = site.get_category_by_name(request['category'])
        # new_course = site.add_courses(request['course_name'], category)
        mapper_course.insert(course)

    # print(request)
    response = render('new_course.html', routes=routes, title=title, categories=categories, name_copy=name_copy,
                      category_copy=category_copy)
    return '200 OK', response.encode()


@application.add_route('/copy_course/')
def copy_course(request):
    title = 'Главная страница'
    logger.log(title)

    # копирование уже существующего курса:
    # copy_course = site.get_course_by_name(request['name_copy'])
    # print(copy_course)
    mapper = MapperRegistry.get_current_mapper('course')
    copy_course = mapper.find_by_id(request['name_copy'])

    new_course = copy_course.clone()
    new_course.course_name = 'new ' + new_course.course_name
    mapper.insert(new_course)

    mapper_course = MapperRegistry.get_current_mapper('course')
    courses = mapper_course.find_all()

    mapper_category = MapperRegistry.get_current_mapper('category')
    categories = mapper_category.find_all()

    response = render('index.html', routes=routes, title=title, courses=courses, categories=categories)
    return '200 OK', response.encode()


@application.add_route('/edit_course/')
def edit_course(request):
    title = 'Изменение курса'
    logger.log(title)
    print(request)

    # new_category = ''
    # course = None
    mapper_category = MapperRegistry.get_current_mapper('category')
    categories = mapper_category.find_all()

    mapper_course = MapperRegistry.get_current_mapper('course')
    course = mapper_course.find_by_id(request['course_id'])

    if request['method'] == 'POST':
        new_course_name = request['new_course_name'].replace('+', ' ')
        course.course_name = new_course_name

        course.category_id = request['category_id']
        mapper_course.update(course)
        course.notify()

        response = render('index.html', routes=routes, title=title, site=site)
    # копирование данных выбранного для изменения курса:
    if request['method'] == 'GET':
        response = render('edit_course.html', routes=routes, title=title, course=course, categories=categories)

    return '200 OK', response.encode()


@application.add_route('/new_category/')
def new_category(request):
    title = 'Создание новой категории'
    logger.log(title)
    if request['method'] == 'POST':
        print(request)
        # site.add_categories(request['category'])
        mapper = MapperRegistry.get_current_mapper('category')
        category = Category(request['category'])
        mapper.insert(category)
    response = render('new_category.html', routes=routes, title=title, site=site)
    return '200 OK', response.encode()


with make_server('', 8000, application) as httpd:
    print("Serving on port 8000...")
    httpd.serve_forever()
