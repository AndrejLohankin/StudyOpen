import pytest
from rest_framework.test import APIClient
from model_bakery import baker
from django.urls import reverse
from rest_framework import status
from students.models import Course, Student



@pytest.fixture
def api_client():
    """Фикстура для API клиента DRF."""
    return APIClient()


@pytest.fixture
def course_factory():
    """Фикстура для фабрики курсов."""
    def _course_factory(**kwargs):
        return baker.make(Course, **kwargs)
    return _course_factory


@pytest.fixture
def student_factory():
    """Фикстура для фабрики студентов."""
    def _student_factory(**kwargs):
        return baker.make(Student, **kwargs)
    return _student_factory


@pytest.mark.django_db
def test_retrieve_course(api_client, course_factory):
    """Тест получения первого курса (retrieve-логика)."""
    course = course_factory()
    url = reverse('courses-detail', kwargs={'pk': course.id})
    response = api_client.get(url)

    assert response.status_code == status.HTTP_200_OK
    assert response.data['id'] == course.id
    assert response.data['name'] == course.name


@pytest.mark.django_db
def test_list_courses(api_client, course_factory):
    """Тест получения списка курсов (list-логика)."""
    courses = course_factory(_quantity=3)
    url = reverse('courses-list')
    response = api_client.get(url)

    assert response.status_code == status.HTTP_200_OK
    assert len(response.data) == len(courses)


@pytest.mark.django_db
def test_filter_courses_by_id(api_client, course_factory):
    """Тест фильтрации списка курсов по id."""
    course = course_factory()
    other_courses = course_factory(_quantity=2)
    url = reverse('courses-list')
    response = api_client.get(url, data={'id': course.id})

    assert response.status_code == status.HTTP_200_OK
    assert len(response.data) == 1
    assert response.data[0]['id'] == course.id


@pytest.mark.django_db
def test_filter_courses_by_name(api_client, course_factory):
    """Тест фильтрации списка курсов по name."""
    course = course_factory(name="Python Programming")
    other_courses = course_factory(_quantity=2)
    url = reverse('courses-list')
    response = api_client.get(url, data={'name': course.name})

    assert response.status_code == status.HTTP_200_OK
    assert len(response.data) == 1
    assert response.data[0]['name'] == course.name


@pytest.mark.django_db
def test_create_course(api_client):
    """Тест успешного создания курса."""
    url = reverse('courses-list')
    data = {'name': 'New Course', 'students': []}
    response = api_client.post(url, data, format='json')

    assert response.status_code == status.HTTP_201_CREATED
    assert Course.objects.count() == 1
    assert Course.objects.get().name == 'New Course'


@pytest.mark.django_db
def test_update_course(api_client, course_factory):
    """Тест успешного обновления курса."""
    course = course_factory()
    url = reverse('courses-detail', kwargs={'pk': course.id})
    updated_data = {'name': 'Updated Course Name', 'students': []}
    response = api_client.put(url, updated_data, format='json')

    assert response.status_code == status.HTTP_200_OK
    course.refresh_from_db()
    assert course.name == 'Updated Course Name'


@pytest.mark.django_db
def test_delete_course(api_client, course_factory):
    """Тест успешного удаления курса."""
    course = course_factory()
    url = reverse('courses-detail', kwargs={'pk': course.id})
    response = api_client.delete(url)

    assert response.status_code == status.HTTP_204_NO_CONTENT
    assert Course.objects.count() == 0


@pytest.mark.django_db
@pytest.mark.parametrize("num_students, expected_status", [
    (19, status.HTTP_200_OK),
    (20, status.HTTP_200_OK),
    (21, status.HTTP_400_BAD_REQUEST),
])
def test_student_limit_per_course_parametrized(api_client, settings, course_factory, student_factory, num_students, expected_status):
    """
    Тестирует ограничение на максимальное число студентов на курсе с помощью параметризации.
    Использует фикстуру settings для изменения MAX_STUDENTS_PER_COURSE.
    Проверяет лимит при обновлении списка студентов через PUT запрос.
    """
    settings.MAX_STUDENTS_PER_COURSE = 20
    course = course_factory()
    students = student_factory(_quantity=num_students)
    url = reverse('courses-detail', kwargs={'pk': course.id})

    update_data = {'name': course.name, 'students': [student.id for student in students]}

    response = api_client.put(url, update_data, format='json')

    assert response.status_code == expected_status

    if expected_status == status.HTTP_400_BAD_REQUEST:
        course.refresh_from_db()
        assert course.students.count() == 0
    elif expected_status == status.HTTP_200_OK:
        course.refresh_from_db()
        assert course.students.count() == num_students