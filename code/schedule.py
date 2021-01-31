import os
import sqlite3

if os.path.isfile('schedule.db'):
    conn = sqlite3.connect('schedule.db')
    conn.text_factory=str
    cur = conn.cursor()


    def _close_db():
        conn.commit()
        conn.close()


    def print_table(list_of_tuples):
        for item in list_of_tuples:
            print(item)


    def print_tables():
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


    def assign_course_to_classroom(iteration, classroom_row):
        cur.execute("""
                    SELECT * FROM  courses WHERE class_id =(?)
                    """,[classroom_row[0]])
        course = cur.fetchone()
        if course is not None:  # check syntax
            print('({}) {}: {} is schedule to start'.format(iteration, classroom_row[1].strip(), course[1]))
            cur.execute("""
                        UPDATE classrooms SET current_course_id=(?), current_course_time_left=(?) WHERE id=(?)
                        """, [course[0], course[5], classroom_row[0]])
            cur.execute("""
                        SELECT * FROM  students WHERE grade =(?)
                        """, [course[2]])
            student_row = cur.fetchone()  # select according primary key
            cur.execute("""
                          UPDATE students SET count=(?) WHERE grade=(?)
                      """, [student_row[1]-course[3],course[2].strip()])


    def occupied_classroom(iteration, classroom_row):
        cur.execute("""
                    SELECT course_name FROM  courses WHERE id =(?)
                    """, [classroom_row[2]])
        course_name = cur.fetchone()
        print('({}) {}: occupied by {}'.format(iteration, classroom_row[1].strip(), course_name[0].strip()))
        cur.execute("""
                    UPDATE classrooms SET current_course_time_left=(?) WHERE id=(?)
                    """, [classroom_row[3]-1, classroom_row[0]])


    def remove_and_assign_course(iteration, classroom_row):
        cur.execute("""
                    SELECT course_name FROM  courses WHERE id =(?)
                    """, [classroom_row[2]])
        course_name = cur.fetchone()
        print('({}) {}: {} is done'.format(iteration, classroom_row[1].strip(), course_name[0].strip()))
        cur.execute("""
                    DELETE FROM courses WHERE id=(?)
                    """, [classroom_row[2]])
        cur.execute("""
                    UPDATE classrooms SET current_course_id=(?), current_course_time_left=(?) WHERE id=(?)
                    """, [0, 0, classroom_row[0]])
        #classroom_row[2] = 0
        #classroom_row[3] = 0
        assign_course_to_classroom(iteration, classroom_row)


    def main():
            cur.execute("""
              SELECT * FROM  courses
            """)
            list_of_courses = cur.fetchall()
            iteration = 0
            if len(list_of_courses) == 0:
                print_tables()
            while not len(list_of_courses) == 0:
                cur.execute("""
                SELECT * FROM  classrooms
                """)
                for classroom_row in cur.fetchall():
                    if classroom_row[3] == 0:
                        assign_course_to_classroom(iteration, classroom_row)
                    if classroom_row[3] > 1:
                        occupied_classroom(iteration, classroom_row)
                    if classroom_row[3] == 1:
                        remove_and_assign_course(iteration, classroom_row)
                print_tables()
                cur.execute("""
                              SELECT * FROM  courses
                            """)
                list_of_courses = cur.fetchall()
                iteration = iteration +1
            _close_db()

    if __name__ == '__main__':
        main()
