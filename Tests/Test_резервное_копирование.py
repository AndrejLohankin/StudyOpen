import pytest
import requests
import uuid
import os
from dotenv import load_dotenv
from Резервное_копирование import put_folder


load_dotenv()
class TestYandexDiskAPIRealCalls:
    """
    Тесты, выполняющие реальные вызовы к API Яндекс.Диска.
    Требуется действующий OAuth-токен.
    """

    @pytest.fixture(scope="class")
    def yandex_token(self):
        """Фикстура для получения токена.
           Установите переменную окружения YANDEX_DISK_TOKEN или вставьте токен напрямую.
        """
        token = os.getenv('YANDEX_DISK_TOKEN')
        if not token:
            pytest.skip("Требуется YANDEX_DISK_TOKEN в переменных окружения")
        return token

    @pytest.fixture
    def unique_folder_name(self):
        """Фикстура для генерации уникального имени папки для каждого теста."""
        return f"test_folder_{uuid.uuid4().hex[:8]}"

    def test_yandex_api_status_accessible(self, yandex_token):
        """Проверка общей доступности API Яндекс.Диска."""
        url = 'https://cloud-api.yandex.net/v1/disk/resources'
        headers = {'Authorization': yandex_token}
        # Простой запрос к корню диска
        response = requests.get(url, headers=headers, params={'path': '/'})

        # Утверждение: Код статуса должен быть 200 (OK)
        assert response.status_code == 200, f"API недоступен. Код: {response.status_code}, Ответ: {response.text}"

    def test_create_folder_success(self, yandex_token, unique_folder_name):
        """Позитивный тест: успешное создание папки."""
        url = 'https://cloud-api.yandex.net/v1/disk/resources'
        headers = {'Authorization': yandex_token}
        params = {'path': unique_folder_name}

        # --- Действие: Создание папки ---
        response = requests.put(url, headers=headers, params=params)

        # --- Утверждения ---
        # 1. Код ответа должен быть 201 (Created) или 409 (Conflict, если уже существует, маловероятно с UUID)
        assert response.status_code in [201,
                                        409], f"Не удалось создать папку. Код: {response.status_code}, Ответ: {response.text}"
        if response.status_code == 201:
            print(f"\nПапка '{unique_folder_name}' успешно создана.")
        elif response.status_code == 409:
            print(f"\nПапка '{unique_folder_name}' уже существует (редко, но возможно).")

    def test_created_folder_appears_in_list(self, yandex_token, unique_folder_name):
        """Позитивный тест: созданная папка появляется в списке файлов."""
        # Сначала создадим папку, чтобы убедиться, что она существует для проверки
        create_url = 'https://cloud-api.yandex.net/v1/disk/resources'
        create_headers = {'Authorization': yandex_token}
        create_params = {'path': unique_folder_name}
        requests.put(create_url, headers=create_headers,
                     params=create_params)  # Игнорируем результат, фокус на проверке

        # --- Действие: Получение списка файлов ---
        list_url = 'https://cloud-api.yandex.net/v1/disk/resources'
        list_headers = {'Authorization': yandex_token}
        list_params = {'path': '/'}
        response = requests.get(list_url, headers=list_headers, params=list_params)

        # --- Утверждения ---
        assert response.status_code == 200, f"Не удалось получить список файлов. Код: {response.status_code}, Ответ: {response.text}"

        data = response.json()
        items = data.get('_embedded', {}).get('items', [])

        # Проверяем, что папка с нужным именем есть в списке
        folder_names = [item.get('name') for item in items if item.get('type') == 'dir']
        assert unique_folder_name in folder_names, f"Созданная папка '{unique_folder_name}' не найдена в списке директорий."

    @pytest.mark.parametrize("invalid_token", [
        "AgAAAAA_invalid_token_12345",
        "Bearer invalid_token_xyz",
        "invalid_format",
        "",  # Пустой токен
    ])
    def test_create_folder_invalid_token(self, invalid_token, unique_folder_name):
        """Негативный тест: попытка создания папки с невалидным токеном."""
        url = 'https://cloud-api.yandex.net/v1/disk/resources'
        headers = {'Authorization': invalid_token}
        params = {'path': unique_folder_name}

        # --- Действие: Попытка создания папки с невалидным токеном ---
        response = requests.put(url, headers=headers, params=params)

        # --- Утверждение ---
        # Ожидаем код ошибки авторизации
        assert response.status_code == 401, f"Ожидался код 401 для невалидного токена, но получен {response.status_code}. Ответ: {response.text}"
        print(f"\nПопытка с токеном '{invalid_token}' корректно отклонена с кодом 401.")

    def test_create_folder_empty_name(self, yandex_token):
        """Негативный тест: попытка создания папки с пустым именем."""
        url = 'https://cloud-api.yandex.net/v1/disk/resources'
        headers = {'Authorization': yandex_token}
        params = {'path': ''}  # Пустое имя

        # --- Действие ---
        response = requests.put(url, headers=headers, params=params)

        # --- Утверждение ---
        # Ожидаем ошибку запроса
        assert response.status_code == 400, f"Ожидался код 400 для пустого имени, но получен {response.status_code}. Ответ: {response.text}"
        print(f"\nПопытка создать папку с пустым именем корректно отклонена с кодом 400.")

    def test_dog_ceo_api_accessible(self):
        """Проверка доступности API Dog CEO."""
        url = 'https://dog.ceo/api/breeds/image/random'

        # --- Действие ---
        response = requests.get(url)

        # --- Утверждение ---
        assert response.status_code == 200, f"API Dog CEO недоступен. Код: {response.status_code}, Ответ: {response.text}"
        data = response.json()
        assert data.get('status') == 'success', f"API Dog CEO вернул статус не success: {data}"
        assert 'message' in data, "Ответ API Dog CEO не содержит ключ 'message'"
        print(f"\nDog CEO API доступен. Получено изображение: {data['message'][:50]}...")


    def test_put_folder_integration(self, yandex_token, unique_folder_name):
        """Интеграционный тест для функции put_folder."""
        try:
            put_folder(unique_folder_name, yandex_token)
            list_url = 'https://cloud-api.yandex.net/v1/disk/resources'
            headers = {'Authorization': yandex_token}
            params = {'path': '/'}
            list_response = requests.get(list_url, headers=headers, params=params)
            items = list_response.json().get('_embedded', {}).get('items', [])
            folder_names = [item.get('name') for item in items if item.get('type') == 'dir']
            assert unique_folder_name in folder_names
        except Exception as e:
            pytest.fail(f"Функция put_folder вызвала исключение: {e}")

