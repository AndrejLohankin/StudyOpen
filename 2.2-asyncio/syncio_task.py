import time
import urllib.request
import json
import psycopg2
import logging
from typing import Dict, Any

# Настройка логирования
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

# Конфигурация подключения к БД
DB_CONFIG = {
    'host': 'localhost',
    'port': 5432,
    'database': 'starwars_db_pg',
    'user': 'postgres',
    'password': 'your_password'
}

# SQL для создания таблицы
CREATE_TABLE_QUERY = """
CREATE TABLE IF NOT EXISTS characters (
    id INTEGER PRIMARY KEY,
    birth_year VARCHAR(20),
    eye_color VARCHAR(50),
    gender VARCHAR(50),
    hair_color VARCHAR(50),
    homeworld TEXT,
    mass VARCHAR(20),
    name VARCHAR(255),
    skin_color VARCHAR(50)
);
"""


def create_table():
    """Создание таблицы персонажей"""
    conn = psycopg2.connect(**DB_CONFIG)
    try:
        with conn.cursor() as cur:
            cur.execute(CREATE_TABLE_QUERY)
        conn.commit()
        logger.info("Таблица characters создана")
    finally:
        conn.close()


def fetch_character_sync(character_id: int) -> Dict[str, Any]:
    """Получение данных одного персонажа синхронно"""
    url = f"https://www.swapi.tech/api/people/{character_id}"
    try:
        with urllib.request.urlopen(url) as response:
            if response.status == 200:
                data = json.loads(response.read().decode())
                props = data['result']['properties']

                return {
                    'id': int(data['result']['uid']),
                    'birth_year': props.get('birth_year'),
                    'eye_color': props.get('eye_color'),
                    'gender': props.get('gender'),
                    'hair_color': props.get('hair_color'),
                    'homeworld': props.get('homeworld'),
                    'mass': props.get('mass'),
                    'name': props.get('name'),
                    'skin_color': props.get('skin_color')
                }
            else:
                logger.warning(f"Ошибка при получении персонажа {character_id}: {response.status}")
                return None
    except Exception as e:
        logger.error(f"Исключение при получении персонажа {character_id}: {e}")
        return None


def save_character(conn, character: Dict[str, Any]):
    """Сохранение персонажа в БД"""
    query = """
    INSERT INTO characters (id, birth_year, eye_color, gender, hair_color, homeworld, mass, name, skin_color)
    VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s)
    ON CONFLICT (id) DO UPDATE SET
        birth_year = EXCLUDED.birth_year,
        eye_color = EXCLUDED.eye_color,
        gender = EXCLUDED.gender,
        hair_color = EXCLUDED.hair_color,
        homeworld = EXCLUDED.homeworld,
        mass = EXCLUDED.mass,
        name = EXCLUDED.name,
        skin_color = EXCLUDED.skin_color;
    """

    with conn.cursor() as cur:
        cur.execute(query, (
            character['id'],
            character['birth_year'],
            character['eye_color'],
            character['gender'],
            character['hair_color'],
            character['homeworld'],
            character['mass'],
            character['name'],
            character['skin_color']
        ))


def main():
    # Создание таблицы
    create_table()


    max_char_id = 83

    # Синхронное получение и сохранение всех персонажей
    conn = psycopg2.connect(**DB_CONFIG)
    try:
        success_count = 0
        for i in range(1, max_char_id + 1):
            character = fetch_character_sync(i)
            if character:
                save_character(conn, character)
                success_count += 1

        conn.commit()
        logger.info(f"Загружено {success_count} персонажей")
    finally:
        conn.close()


if __name__ == "__main__":
    start_time = time.time()
    main()
    end_time = time.time()
    elapsed_time = end_time - start_time

    print(f"Время выполнения синхронного скрипта: {elapsed_time:.2f} секунд")
