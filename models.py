# фабричный метод для пользователей
class UsersCreator():
    @staticmethod
    def create_user(user_type, name, last_name):
        user_types = {
            'student': Student,
            'teacher': Teacher
        }
        return user_types[user_type](name, last_name)


class User:
    def __init__(self, name, last_name):
        self.name = name
        self.last_name = last_name


class Student(User):
    pass


class Teacher(User):
    pass


class Course:
    # Список пользователей записанных на курс
    users = []

    def __init__(self, course_name, category):
        # Название курса
        self.course_name = course_name
        # объект категории к которой относится курс
        self.category = category

    # добавление нового пользователя на курс
    def add_user(self, user: User):
        self.users.append(user)

    def __repr__(self):
        return self.course_name


class Category:
    def __init__(self, category_name):
        # Название категории
        self.category_name = category_name

    def __repr__(self):
        return self.category_name


# Основной класс сайта
class Website:
    users = []
    categories = []
    courses = []

    def add_user(self, type, name, last_name):
        new_user = UsersCreator.create_user(type, name, last_name)
        self.users.append(new_user)
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
