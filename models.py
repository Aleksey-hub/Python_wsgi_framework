from orm.unitofwork import DomainObject
from reusepatterns.observer import Subject, Observer
from reusepatterns.prototype import PrototypeMixin


# фабричный метод для пользователей
class User:
    def __init__(self, first_name, last_name):
        self.first_name = first_name
        self.last_name = last_name


class Student(User, Observer, DomainObject):
    def update(self, subject):
        print(f'SMS-> {self.first_name} {self.last_name}: Произошли изменения на курсе "{subject.course_name}"')
        print(f'EMAIL-> {self.first_name} {self.last_name}: Произошли изменения на курсе "{subject.course_name}"')


class Teacher(User, Observer, DomainObject):
    def update(self, subject):
        print(f'SMS-> {self.first_name} {self.last_name}: Произошли изменения на курсе "{subject.course_name}"')
        print(f'EMAIL-> {self.first_name} {self.last_name}: Произошли изменения на курсе "{subject.course_name}"')


class UsersCreator:
    user_types = {
        'student': Student,
        'teacher': Teacher
    }

    @classmethod
    def create_user(cls, user_type, name, last_name):
        return cls.user_types[user_type](name, last_name)


class Course(PrototypeMixin, Subject, DomainObject):
    # Список пользователей записанных на курс
    # users = []
    # список студентов записанных на курс
    students = []
    # список преподавателей
    teachers = []
    # наличие преподавателя на курсе
    teacher = False

    def __init__(self, course_name, category_id):
        # Название курса
        self.course_name = course_name
        # категория к которой относится курс
        self.category_id = category_id
        super().__init__()

    # добавление нового пользователя на курс
    def add_user(self, user: User):
        if self.teacher and isinstance(user, Teacher):
            print('На курсе уже есть преподаватель.')
        elif isinstance(user, Teacher):
            self.teachers.append(user)
            self.teacher = True
            self.attach(user)
        else:
            self.students.append(user)
            self.attach(user)

    def __repr__(self):
        return self.course_name


class Category(DomainObject):
    def __init__(self, category_name):
        # Название категории
        self.category_name = category_name

    def __repr__(self):
        return self.category_name


class CoursesStudents(DomainObject):
    def __init__(self, course_id, student_id):
        self.course_id = course_id
        self.student_id = student_id


# Основной класс сайта
class Website:
    # users = []
    # список студентов
    students = []
    # список преподавателей
    teachers = []
    categories = []
    courses = []

    def add_user(self, type, name, last_name):
        new_user = UsersCreator.create_user(type, name, last_name)
        if type == 'student':
            self.students.append(new_user)
        elif type == 'teacher':
            self.teachers.append(new_user)
        else:
            print('Неверный тип пользователя.')
        return new_user

    def add_categories(self, category_name):
        new_category = Category(category_name)
        self.categories.append(new_category)
        return new_category

    def add_courses(self, course_name, category):
        new_course = Course(course_name, category)
        self.courses.append(new_course)
        return new_course

    def get_category_by_name(self, category_name):
        for category in self.categories:
            if category.category_name == category_name:
                return category

    def get_course_by_name(self, course_name):
        for course in self.courses:
            if course.course_name == course_name:
                return course

    def get_student_by_name(self, name, last_name):
        for student in self.students:
            if name == student.first_name and last_name == student.last_name:
                return student


if __name__ == '__main__':
    site = Website()

    student1 = site.add_user('student', 'Иван', 'Иванов')
    categories1 = site.add_categories('Python')
    course1 = site.add_courses('Python для профессионалов', categories1)

    course1.add_user(student1)
    print(student1)

    teacher1 = site.add_user('teacher', 'Дмитрий', 'Иванов')
    course1.add_user(teacher1)
    print(teacher1)
    print(site.courses)
    isinstance()
