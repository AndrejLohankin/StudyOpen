import pytest

# Импортируем необходимые данные и логику
from Task_3 import courses, mentors, durations  # замените your_module на имя вашего файла без .py


@pytest.mark.parametrize(
    "input_courses, input_mentors, input_durations, expected_order",
    [
        # Основной тест из примера
        (
                ["Java-разработчик с нуля", "Fullstack-разработчик на Python", "Python-разработчик с нуля",
                 "Frontend-разработчик с нуля"],
                [
                    ["Филипп Воронов", "Анна Юшина"],  # сокращенные списки для теста
                    ["Евгений Шмаргунов", "Олег Булыгин"],
                    ["Евгений Шмаргунов", "Олег Булыгин"],
                    ["Владимир Чебукин", "Эдгар Нуруллин"]
                ],
                [14, 20, 12, 20],
                ["Python-разработчик с нуля", "Java-разработчик с нуля", "Fullstack-разработчик на Python",
                 "Frontend-разработчик с нуля"]
        ),
        # Тест с уникальными длительностями
        (
                ["Курс A", "Курс B", "Курс C"],
                [["Ментор 1"], ["Ментор 2"], ["Ментор 3"]],
                [10, 5, 15],
                ["Курс B", "Курс A", "Курс C"]  # 5, 10, 15
        ),
        # Тест с одинаковыми длительностями
        (
                ["Курс X", "Курс Y", "Курс Z"],
                [["Ментор 1"], ["Ментор 2"], ["Ментор 3"]],
                [10, 10, 10],
                ["Курс X", "Курс Y", "Курс Z"]  # порядок как в исходном списке
        ),
        # Тест с одним курсом
        (
                ["Один курс"],
                [["Ментор 1", "Ментор 2"]],
                [8],
                ["Один курс"]
        )
    ]
)
def test_course_sorting(input_courses, input_mentors, input_durations, expected_order):
    # Повторяем логику из основной программы
    courses_list = []
    for course, mentor, duration in zip(input_courses, input_mentors, input_durations):
        course_dict = {"title": course, "mentors": mentor, "duration": duration}
        courses_list.append(course_dict)

    # Сортируем длительности курсов
    durations_dict = {}
    for id, course in enumerate(courses_list):
        key = course["duration"]
        durations_dict.setdefault(key, [])
        durations_dict[key].append(id)

    # Сортируем словарь по ключам
    durations_dict = dict(sorted(durations_dict.items()))

    # Получаем отсортированный список курсов
    result_order = []
    for duration, ids in durations_dict.items():
        for id in ids:
            result_order.append(courses_list[id]["title"])

    assert result_order == expected_order


# Тест для проверки структуры данных courses_list
def test_courses_list_structure():
    # Повторяем создание courses_list
    courses_list = []
    for course, mentor, duration in zip(courses, mentors, durations):
        course_dict = {"title": course, "mentors": mentor, "duration": duration}
        courses_list.append(course_dict)

    # Проверяем структуру
    assert len(courses_list) == 4
    assert courses_list[0]["title"] == "Java-разработчик с нуля"
    assert courses_list[0]["mentors"] == mentors[0]
    assert courses_list[0]["duration"] == 14
    assert isinstance(courses_list[0]["mentors"], list)


# Тест для проверки словаря длительностей
def test_durations_dict():
    # Повторяем создание courses_list
    courses_list = []
    for course, mentor, duration in zip(courses, mentors, durations):
        course_dict = {"title": course, "mentors": mentor, "duration": duration}
        courses_list.append(course_dict)

    # Создаем словарь длительностей
    durations_dict = {}
    for id, course in enumerate(courses_list):
        key = course["duration"]
        durations_dict.setdefault(key, [])
        durations_dict[key].append(id)

    # Проверяем, что словарь создан правильно
    assert 12 in durations_dict  # Python-разработчик с нуля
    assert 14 in durations_dict  # Java-разработчик с нуля
    assert 20 in durations_dict  # Fullstack и Frontend
    assert len(durations_dict[20]) == 2  # два курса по 20 месяцев


# Параметризованный тест для проверки конкретных курсов в отсортированном порядке
@pytest.mark.parametrize(
    "duration, expected_courses",
    [
        (12, ["Python-разработчик с нуля"]),
        (14, ["Java-разработчик с нуля"]),
        (20, ["Fullstack-разработчик на Python", "Frontend-разработчик с нуля"])
    ]
)
def test_specific_durations(duration, expected_courses):
    # Повторяем логику из основной программы
    courses_list = []
    for course, mentor, duration_course in zip(courses, mentors, durations):
        course_dict = {"title": course, "mentors": mentor, "duration": duration_course}
        courses_list.append(course_dict)

    # Создаем и сортируем словарь длительностей
    durations_dict = {}
    for id, course in enumerate(courses_list):
        key = course["duration"]
        durations_dict.setdefault(key, [])
        durations_dict[key].append(id)

    durations_dict = dict(sorted(durations_dict.items()))

    # Проверяем конкретные длительности
    if duration in durations_dict:
        course_titles = [courses_list[id]["title"] for id in durations_dict[duration]]
        assert course_titles == expected_courses
    else:
        assert expected_courses == []