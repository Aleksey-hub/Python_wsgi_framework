BEGIN TRANSACTION;

DROP TABLE IF EXISTS students;
CREATE TABLE students
(
    id         INTEGER PRIMARY KEY AUTOINCREMENT NOT NULL UNIQUE,
    first_name VARCHAR(32),
    last_name  VARCHAR(32)
);

INSERT INTO students (first_name, last_name)
VALUES ('Ivan', 'Ivanov');
INSERT INTO students (first_name, last_name)
VALUES ('Dmitry', 'Ivanov');


DROP TABLE IF EXISTS categories;
CREATE TABLE categories
(
    id            INTEGER PRIMARY KEY AUTOINCREMENT NOT NULL UNIQUE,
    category_name VARCHAR(32)
);

INSERT INTO categories (category_name)
VALUES ('Python');
INSERT INTO categories (category_name)
VALUES ('Java');


DROP TABLE IF EXISTS courses;
CREATE TABLE courses
(
    id          INTEGER PRIMARY KEY AUTOINCREMENT NOT NULL UNIQUE,
    course_name VARCHAR(32),
    category_id INTEGER,
    FOREIGN KEY (category_id) REFERENCES categories (id)
);

INSERT INTO courses (course_name, category_id)
VALUES ('Python for professionals', 1);
INSERT INTO courses (course_name, category_id)
VALUES ('Python for beginners', 1);


DROP TABLE IF EXISTS courses_students;
CREATE TABLE courses_students
(
    id         INTEGER PRIMARY KEY AUTOINCREMENT NOT NULL UNIQUE,
    course_id  INTEGER,
    student_id INTEGER,
    FOREIGN KEY (course_id) REFERENCES courses (id),
    FOREIGN KEY (student_id) REFERENCES students (id)
);

INSERT INTO courses_students (course_id, student_id)
VALUES (1, 1);

COMMIT TRANSACTION;