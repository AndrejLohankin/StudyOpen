class Student:
    def __init__(self, name, surname, gender):
        self.name = name
        self.surname = surname
        self.gender = gender
        self.finished_courses = []
        self.courses_in_progress = []
        self.grades = {}

    def rate_lecture(self, lecturer, course, grade):  # студент оценивает лектора
        if isinstance(lecturer, Lecturer) and course in lecturer.courses_attached \
                and course in self.courses_in_progress or course in self.finished_courses:
            if course in lecturer.grades:
                lecturer.grades[course] += grade
            else:
                lecturer.grades[course] = grade
        else:
            return 'Ошибка'

    def average_grade(self):  # средняя оценка
        grade_list = []
        for grade in self.grades.values():
            grade_list.append((sum(grade) / len(grade)))
        return round((sum(grade_list) / len(grade_list)),2)

    def __str__(self):
        return (f"Name: {self.name} \n"
                f"Surname: {self.surname} \n"
                f"Средняя оценка за домашние задания: {self.average_grade()} \n"
                f"Курсы в процессе изучения: {self.courses_in_progress} \n"
                f"Завершенные курсы: {self.finished_courses}")

    def __eq__(self, student):
       return self.average_grade() == student.average_grade()

    def __gt__(self, student):
       return self.average_grade() > student.average_grade()

    def __lt__(self, student):
       return self.average_grade() < student.average_grade()


class Mentor:
    def __init__(self, name, surname):
        self.name = name
        self.surname = surname
        self.courses_attached = []


class Lecturer(Mentor):
    def __init__(self, name, surname):
        super().__init__(name, surname)
        self.courses_attached = []
        self.grades = {}

    def average_grade(self):  # средняя оценка
        grade_list = []
        for grade in self.grades.values():
            grade_list.append((sum(grade) / len(grade)))
        return round((sum(grade_list) / len(grade_list)),2)

    def __str__(self):
        return (f"Name: {self.name} \n"
                f"Surname: {self.surname} \n"
                f"Средняя оценка за лекции: {self.average_grade()}")

    def __eq__(self, lecturer):
       return self.average_grade() == lecturer.average_grade()

    def __gt__(self, lecturer):
       return self.average_grade() > lecturer.average_grade()

    def __lt__(self, lecturer):
       return self.average_grade() < lecturer.average_grade()


class Reviewer(Mentor):
    def __init__(self, name, surname):
        super().__init__(name, surname)
        self.courses_attached = []

    def rate_hw(self, student, course, grade):  # ревьюер оценивает студента
        if isinstance(student, Student) and course in self.courses_attached \
                and course in student.courses_in_progress or course in student.finished_courses:
            if course in student.grades:
                student.grades[course] += grade
            else:
                student.grades[course] = grade
        else:
            return 'Ошибка'

    def __str__(self):
        return (f"Name: {self.name} /n"
                f"Surname: {self.surname}")


def rate_average_students(students_list, course):  # подсчет средней оценки за домашние задания по всем студентам в рамках курса
    each_grade_list = []
    for student in students_list:
        student_grades = [student.grades[course]]
        for each_student_grade in student_grades:
            for each_grade in each_student_grade:
                each_grade_list.append(each_grade)
    return f"Средний балл по курсу '{course}'\
составляет: {round((sum(each_grade_list)/len(each_grade_list)),2)}"

def rate_average_lecturer(lecturers_list, course):  # подсчет средней оценки за лекции всех лекторов в рамках курса
    each_grade_list = []
    for lecturer in lecturers_list:
        lecturer_grades = [lecturer.grades[course]]
        for each_lecturer_grade in lecturer_grades:
            for each_grade in each_lecturer_grade:
                each_grade_list.append(each_grade)
    return f"Средний балл по курсу '{course}'\
составляет: {round((sum(each_grade_list)/len(each_grade_list)),2)}"


student_1 = Student('Ilya', 'Shatalov', 'M')
student_1.finished_courses += ['PD FPY']
student_1.finished_courses += ['Git']
student_1.courses_in_progress += ['OOP']
student_2 = Student('Julia', 'Markelova', 'F')
student_2.finished_courses += ['PD FPY']
student_2.finished_courses += ['Git']
student_2.courses_in_progress += ['OOP']

lecturer_1 = Lecturer('Andrei', 'Vetrov')
lecturer_1.courses_attached = ['PD FPY']
lecturer_2 = Lecturer('Anastasia', 'Petrova')
lecturer_2.courses_attached = ['Git']
lecturer_3 = Lecturer('Sergei', 'Svyatov')
lecturer_3.courses_attached = ['PD FPY']
lecturer_4 = Lecturer('Vladislav', 'Samoletov')
lecturer_4.courses_attached = ['Git']

reviewer_1 = Reviewer('Artyom', 'Kalkin')
reviewer_1.courses_attached = ['PD FPY']
reviewer_2 = Reviewer('Lisa', 'Vavilova')
reviewer_2.courses_attached = ['Git']

student_1.rate_lecture(lecturer_1, 'PD FPY', [10, 8, 9])
student_1.rate_lecture(lecturer_2, 'Git', [9, 8, 9])
student_2.rate_lecture(lecturer_1, 'PD FPY', [9, 8, 10])
student_2.rate_lecture(lecturer_2, 'Git', [8, 8, 10])
student_1.rate_lecture(lecturer_3, 'PD FPY', [7, 8, 9])
student_1.rate_lecture(lecturer_4, 'Git', [10, 8, 9])
student_2.rate_lecture(lecturer_3, 'PD FPY', [9, 8, 7])
student_2.rate_lecture(lecturer_4, 'Git', [9, 8, 10])

reviewer_1.rate_hw(student_1, 'PD FPY', [9, 8, 9])
reviewer_1.rate_hw(student_2, 'PD FPY', [9, 9, 9])
reviewer_2.rate_hw(student_1, 'Git', [8, 8, 7])
reviewer_2.rate_hw(student_2, 'Git', [7, 9, 9])

students_list = [student_1, student_2]
lecturers_list_PDFPY = [lecturer_1, lecturer_3]
lecturers_list_Git = [lecturer_2, lecturer_4]

print (student_1)
print (student_2)
print (rate_average_students(students_list, 'PD FPY'))
print (rate_average_students(students_list, 'Git'))

print (lecturer_1)
print (lecturer_2)
print (lecturer_3)
print (lecturer_4)
print (rate_average_lecturer(lecturers_list_PDFPY, 'PD FPY'))
print (rate_average_lecturer(lecturers_list_Git, 'Git'))

print (student_1 == student_2)
print (student_1 > student_2)
print (student_1 < student_2)
print (lecturer_1 == lecturer_4)
print(lecturer_1 > lecturer_4)
print(lecturer_1 < lecturer_4)
