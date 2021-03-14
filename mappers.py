import sqlite3

from models import Student, Category, Course, CoursesStudents

connection = sqlite3.connect('db.sqlite')


class RecordNotFoundException(Exception):
    def __init__(self, message):
        super().__init__(f'Record not found: {message}')


class DbCommitException(Exception):
    def __init__(self, message):
        super().__init__(f'Db commit error: {message}')


class DbUpdateException(Exception):
    def __init__(self, message):
        super().__init__(f'Db update error: {message}')


class DbDeleteException(Exception):
    def __init__(self, message):
        super().__init__(f'Db delete error: {message}')


class StudentMapper:
    """
    Паттерн DATA MAPPER
    Слой преобразования данных
    """

    def __init__(self, connection):
        self.connection = connection
        self.cursor = connection.cursor()
        self.tablename = 'students'

    def find_all(self):
        statement = f"SELECT * FROM {self.tablename}"
        self.cursor.execute(statement)
        result = []
        for item in self.cursor.fetchall():
            id, first_name, last_name = item
            student = Student(first_name, last_name)
            student.id = id
            result.append(student)
        return result

    def find_by_id(self, student_id):
        statement = f"SELECT id, first_name, last_name FROM {self.tablename} WHERE id=?"
        self.cursor.execute(statement, (student_id,))
        result = self.cursor.fetchone()
        print(result)
        if result:
            return Student(*result)
        else:
            raise RecordNotFoundException(f'record with id={student_id} not found')

    def insert(self, student):

        statement = f"INSERT INTO {self.tablename} (first_name, last_name) VALUES (?, ?)"
        self.cursor.execute(statement, (student.first_name, student.last_name))
        try:
            self.connection.commit()
        except Exception as e:
            raise DbCommitException(e.args)

    def update(self, student):
        statement = f"UPDATE {self.tablename} SET first_name=?, last_name=? WHERE id=?"

        self.cursor.execute(statement, (student.first_name, student.last_name,
                                        student.student_id))
        try:
            self.connection.commit()
        except Exception as e:
            raise DbUpdateException(e.args)

    def delete(self, student):
        statement = f"DELETE FROM {self.tablename} WHERE id=?"

        self.cursor.execute(statement, (student.student_id,))
        try:
            self.connection.commit()
        except Exception as e:
            raise DbDeleteException(e.args)


class CategoryMapper:
    def __init__(self, connection):
        self.connection = connection
        self.cursor = connection.cursor()
        self.tablename = 'categories'

    def find_all(self):
        statement = f"SELECT * FROM {self.tablename}"
        self.cursor.execute(statement)
        result = []
        for item in self.cursor.fetchall():
            id, category_name = item
            category = Category(category_name)
            category.id = id
            result.append(category)
        return result

    def find_by_id(self, category_id):
        statement = f"SELECT id, category_name FROM {self.tablename} WHERE id=?"
        self.cursor.execute(statement, (category_id,))
        result = self.cursor.fetchone()
        if result:
            return Category(*result)
        else:
            raise RecordNotFoundException(f'record with id={category_id} not found')

    def insert(self, category):

        statement = f"INSERT INTO {self.tablename} (category_name) VALUES (?)"
        self.cursor.execute(statement, (category.category_name,))
        try:
            self.connection.commit()
        except Exception as e:
            raise DbCommitException(e.args)

    def update(self, category):
        statement = f"UPDATE {self.tablename} SET category_name=? WHERE id=?"

        self.cursor.execute(statement, (category.category_name, category.category_id))
        try:
            self.connection.commit()
        except Exception as e:
            raise DbUpdateException(e.args)

    def delete(self, category):
        statement = f"DELETE FROM {self.tablename} WHERE id=?"

        self.cursor.execute(statement, (category.category_id,))
        try:
            self.connection.commit()
        except Exception as e:
            raise DbDeleteException(e.args)


class CourseMapper:
    def __init__(self, connection):
        self.connection = connection
        self.cursor = connection.cursor()
        self.tablename = 'courses'

    def find_all(self):
        statement = f"SELECT * FROM {self.tablename}"
        self.cursor.execute(statement)
        result = []
        for item in self.cursor.fetchall():
            id, course_name, category_id = item
            course = Course(course_name, category_id)
            course.id = id
            result.append(course)
        return result

    def find_by_id(self, course_id):
        statement = f"SELECT id, course_name, category_id FROM {self.tablename} WHERE id=?"
        self.cursor.execute(statement, (course_id,))
        id, *result = self.cursor.fetchone()
        if result:
            course = Course(*result)
            course.id = id
            return course
        else:
            raise RecordNotFoundException(f'record with id={course_id} not found')

    def insert(self, course):

        statement = f"INSERT INTO {self.tablename} (course_name, category_id) VALUES (?, ?)"
        self.cursor.execute(statement, (course.course_name, course.category_id))
        try:
            self.connection.commit()
        except Exception as e:
            raise DbCommitException(e.args)

    def update(self, course):
        statement = f"UPDATE {self.tablename} SET course_name=?, category_id=? WHERE id=?"

        self.cursor.execute(statement, (course.course_name, course.category_id,
                                        course.id,))
        try:
            self.connection.commit()
        except Exception as e:
            raise DbUpdateException(e.args)

    def delete(self, course):
        statement = f"DELETE FROM {self.tablename} WHERE id=?"

        self.cursor.execute(statement, (course.id,))
        try:
            self.connection.commit()
        except Exception as e:
            raise DbDeleteException(e.args)


class CoursesStudentsMapper:
    def __init__(self, connection):
        self.connection = connection
        self.cursor = connection.cursor()
        self.tablename = 'courses_students'

    def find_all(self):
        statement = f"SELECT * FROM {self.tablename}"
        self.cursor.execute(statement)
        result = []
        for item in self.cursor.fetchall():
            id, course_id, student_id = item
            course_student = CoursesStudents(course_id, student_id)
            course_student.id = id
            result.append(course_student)
        return result

    def find_by_id(self, course_student_id):
        statement = f"SELECT id, course_name, category_id FROM {self.tablename} WHERE id=?"
        self.cursor.execute(statement, (course_student_id,))
        result = self.cursor.fetchone()
        if result:
            return CoursesStudents(*result)
        else:
            raise RecordNotFoundException(f'record with id={course_student_id} not found')

    def insert(self, course_student):

        statement = f"INSERT INTO {self.tablename} (course_id, student_id) VALUES (?, ?)"
        self.cursor.execute(statement, (course_student.course_id, course_student.student_id))
        try:
            self.connection.commit()
        except Exception as e:
            raise DbCommitException(e.args)

    def update(self, course_student):
        statement = f"UPDATE {self.tablename} SET course_id=?, student_id=? WHERE id=?"

        self.cursor.execute(statement, (course_student.course_id, course_student.student_id,
                                        course_student.id))
        try:
            self.connection.commit()
        except Exception as e:
            raise DbUpdateException(e.args)

    def delete(self, course_student):
        statement = f"DELETE FROM {self.tablename} WHERE id=?"

        self.cursor.execute(statement, (course_student.id,))
        try:
            self.connection.commit()
        except Exception as e:
            raise DbDeleteException(e.args)


class MapperRegistry:
    mappers = {
        'student': StudentMapper,
        'category': CategoryMapper,
        'course': CourseMapper,
        'courses_students': CoursesStudentsMapper
    }

    @staticmethod
    def get_mapper(obj):
        if isinstance(obj, Student):
            return StudentMapper(connection)
        if isinstance(obj, Category):
            return CategoryMapper(connection)

    @staticmethod
    def get_current_mapper(name):
        return MapperRegistry.mappers[name](connection)
