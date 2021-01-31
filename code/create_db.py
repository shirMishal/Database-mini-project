import os
import sqlite3
import sys
import atexit


#check if file exist
DBExist = os.path.isfile('schedule.db')
#print(DBExist)
# connect to the database
_conn = sqlite3.connect('schedule.db')
_conn.text_factory=str
#print("connect")


# register a function to be called immediately when the interpreter terminates
def _close_db():
    _conn.commit()
    _conn.close()
    #os.remove('schedule.db')


def create_tables():
    _conn.executescript("""
        CREATE TABLE courses (
            id      INTEGER     PRIMARY KEY,
            course_name    TEXT        NOT NULL,
            student TEXT        NOT NULL,
            number_of_students INTEGER NOT NULL,
            class_id INTEGER REFERENCES classrooms(id),
            course_length INTEGER NOT NULL
        );

        CREATE TABLE students (
            grade       TEXT     PRIMARY KEY,
            count     INTEGER    NOT NULL
        );

        CREATE TABLE classrooms (
            id      INTEGER     PRIMARY KEY,
            location  TEXT     NOT NULL,
            current_course_id            INTEGER     NOT NULL,
            current_course_time_left INTEGER     NOT NULL


        );
    """)
    # FOREIGN KEY(student_id)     REFERENCES students(id),
    # FOREIGN KEY(assignment_num) REFERENCES assignments(num),
    #atexit.register(_close_db)


def put_file_in_tables(input_file_name):
    with open(input_file_name) as input_file:
        for line in input_file:
            line = line.split(',')
            if line[0].strip() == 'S':
                _conn.execute("""
                               INSERT INTO students (grade, count) VALUES (?, ?)
                           """, [line[1].strip(), line[2].strip()])
            elif line[0].strip() == 'R':
                _conn.execute("""
                               INSERT INTO classrooms (id, location, current_course_id, current_course_time_left) VALUES (?, ?,?,?)
                           """, [line[1].strip(), line[2].strip(), 0, 0])
            elif line[0].strip() == 'C':
                _conn.execute("""
                               INSERT INTO courses (id, course_name, student, number_of_students, class_id, course_length) VALUES (?, ?,?,?,?,?)
                           """, [line[1].strip(),line[2].strip(),line[3].strip(),line[4].strip(),line[5].strip(), line[6].strip()])


def print_table(list_of_tuples):
    for item in list_of_tuples:
        print(item)


def print_tables():
    cur = _conn.cursor()
    print("courses")
    all_courses = cur.execute("""
                SELECT * FROM  courses
            """).fetchall()
    print_table(all_courses)
    print("classrooms")
    all_classrooms = cur.execute("""
                    SELECT * FROM  classrooms
                """).fetchall()
    print_table(all_classrooms)
    print("students")
    all_students = cur.execute("""
                    SELECT * FROM  students
                """).fetchall()
    print_table(all_students)
    _close_db()


def main(args):
    if not DBExist:
        create_tables()
        put_file_in_tables(args[1])
        print_tables()


if __name__ == '__main__':
    main(sys.argv)
