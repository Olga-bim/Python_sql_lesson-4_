import enum
import os
import sqlite3


class Menu(enum.Enum):
    ADD_STUDENT = 1
    ADD_COURSE = 2
    VIEW_STUDENTS = 3
    VIEW_COURSES = 4
    EDIT_STUDENT = 5
    EDIT_COURSE = 6
    DELETE_STUDENT = 7
    DELETE_COURSE = 8
    EXIT = 9


def display_menu():
    print("\n1. Add Student")
    print("2. Add Course")
    print("3. View Students")
    print("4. View Courses")
    print("5. Edit Student")
    print("6. Edit Course")
    print("7. Delete Student")
    print("8. Delete Course")
    print("9. Exit")


def add_student(conn):
    name = input("Enter student name: ")
    age = int(input("Enter student age: "))
    grade = input("Enter student grade: ")
    course_name = input("Enter course name: ")

    # Проверяем, существует ли такой курс
    cursor = conn.execute("SELECT id FROM courses WHERE name = ?", (course_name,))
    course = cursor.fetchone()
    
    if course:
        with conn:
            conn.execute("INSERT INTO students (name, age, grade, course_name) VALUES (?, ?, ?, ?)",
                         (name, age, grade, course_name))
            conn.execute("UPDATE courses SET student_count = student_count + 1 WHERE name = ?", (course_name,))
        print("Student added successfully.")
    else:
        print("Course not found. Please add the course first.")


def add_course(conn):
    course_name = input("Enter course name: ")
    with conn:
        conn.execute("INSERT INTO courses (name, student_count) VALUES (?, 0)", (course_name,))
    print("Course added successfully.")


def view_students(conn):
    cursor = conn.execute("SELECT * FROM students")
    for row in cursor:
        print(f"ID: {row[0]}, Name: {row[1]}, Age: {row[2]}, Grade: {row[3]}, Course: {row[4]}")


def view_courses(conn):
    cursor = conn.execute("SELECT * FROM courses")
    for row in cursor:
        print(f"Course ID: {row[0]}, Course Name: {row[1]}, Student Count: {row[2]}")


def edit_student(conn):
    student_id = int(input("Enter student ID to edit: "))
    new_name = input("Enter new student name: ")
    new_age = int(input("Enter new student age: "))
    new_grade = input("Enter new student grade: ")
    new_course_name = input("Enter new course name: ")

    cursor = conn.execute("SELECT course_name FROM students WHERE id = ?", (student_id,))
    old_course_name = cursor.fetchone()[0]

    # Проверяем, существует ли новый курс
    cursor = conn.execute("SELECT id FROM courses WHERE name = ?", (new_course_name,))
    course = cursor.fetchone()

    if course:
        with conn:
            conn.execute("UPDATE students SET name = ?, age = ?, grade = ?, course_name = ? WHERE id = ?",
                         (new_name, new_age, new_grade, new_course_name, student_id))
            conn.execute("UPDATE courses SET student_count = student_count + 1 WHERE name = ?", (new_course_name,))
            if old_course_name != new_course_name:
                conn.execute("UPDATE courses SET student_count = student_count - 1 WHERE name = ?", (old_course_name,))
        print("Student updated successfully.")
    else:
        print("Course not found. Please add the course first.")


def edit_course(conn):
    course_id = int(input("Enter course ID to edit: "))
    new_name = input("Enter new course name: ")
    with conn:
        conn.execute("UPDATE courses SET name = ? WHERE id = ?", (new_name, course_id))
        conn.execute("UPDATE students SET course_name = ? WHERE course_name = (SELECT name FROM courses WHERE id = ?)",
                     (new_name, course_id))
    print("Course updated successfully.")


def delete_student(conn):
    student_id = int(input("Enter student ID to delete: "))

    cursor = conn.execute("SELECT course_name FROM students WHERE id = ?", (student_id,))
    course_name = cursor.fetchone()[0]

    with conn:
        conn.execute("DELETE FROM students WHERE id = ?", (student_id,))
        conn.execute("UPDATE courses SET student_count = student_count - 1 WHERE name = ?", (course_name,))
    print("Student deleted successfully.")


def delete_course(conn):
    course_id = int(input("Enter course ID to delete: "))

    with conn:
        conn.execute("DELETE FROM courses WHERE id = ?", (course_id,))
        conn.execute("DELETE FROM students WHERE course_name = (SELECT name FROM courses WHERE id = ?)", (course_id,))
    print("Course deleted successfully.")


def main():
    conn = sqlite3.connect('school.db')
    conn.execute('''CREATE TABLE IF NOT EXISTS students
                    (id INTEGER PRIMARY KEY AUTOINCREMENT,
                    name TEXT NOT NULL,
                    age INTEGER NOT NULL,
                    grade TEXT NOT NULL,
                    course_name TEXT NOT NULL);''')
    conn.execute('''CREATE TABLE IF NOT EXISTS courses
                    (id INTEGER PRIMARY KEY AUTOINCREMENT,
                    name TEXT NOT NULL,
                    student_count INTEGER DEFAULT 0);''')

    while True:
        display_menu()
        choice = int(input("Enter your choice: "))
        if choice == Menu.ADD_STUDENT.value:
            add_student(conn)
        elif choice == Menu.ADD_COURSE.value:
            add_course(conn)
        elif choice == Menu.VIEW_STUDENTS.value:
            view_students(conn)
        elif choice == Menu.VIEW_COURSES.value:
            view_courses(conn)
        elif choice == Menu.EDIT_STUDENT.value:
            edit_student(conn)
        elif choice == Menu.EDIT_COURSE.value:
            edit_course(conn)
        elif choice == Menu.DELETE_STUDENT.value:
            delete_student(conn)
        elif choice == Menu.DELETE_COURSE.value:
            delete_course(conn)
        elif choice == Menu.EXIT.value:
            print("Exiting...")
            break
        else:
            print("Invalid choice. Please try again.")

    conn.close()


if __name__ == "__main__":
    main()
