import asyncio
import asyncpg
from typing import Dict, List, Any
import logging
import urllib.request
import json
import time


# Настройка логирования
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

# Конфигурация подключения к БД
DB_CONFIG = {
    'host': 'localhost',
    'port': 5432,
    'database': 'starwars_db_pg',
    'user': 'postgres',
    'password': '98199819'
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


async def create_table():
    """Создание таблицы персонажей"""
    conn = await asyncpg.connect(**DB_CONFIG)
    try:
        await conn.execute(CREATE_TABLE_QUERY)
        logger.info("Таблица characters создана")
    finally:
        await conn.close()


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


async def fetch_character_async(character_id: int) -> Dict[str, Any]:
    """Асинхронная обертка для синхронной функции"""
    loop = asyncio.get_event_loop()
    return await loop.run_in_executor(None, fetch_character_sync, character_id)


async def save_character(conn: asyncpg.Connection, character: Dict[str, Any]):
    """Сохранение персонажа в БД"""
    query = """
    INSERT INTO characters (id, birth_year, eye_color, gender, hair_color, homeworld, mass, name, skin_color)
    VALUES ($1, $2, $3, $4, $5, $6, $7, $8, $9)
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

    await conn.execute(
        query,
        character['id'],
        character['birth_year'],
        character['eye_color'],
        character['gender'],
        character['hair_color'],
        character['homeworld'],
        character['mass'],
        character['name'],
        character['skin_color']
    )


async def main():
    # Создание таблицы
    await create_table()

    # Получение максимального ID персонажа
    max_char_id = 83

    # Асинхронное выполнение синхронных запросов
    tasks = [fetch_character_async(i) for i in range(1, max_char_id + 1)]
    characters = await asyncio.gather(*tasks)

    # Фильтрация успешных результатов
    characters = [char for char in characters if char]

    # Сохранение в БД
    conn = await asyncpg.connect(**DB_CONFIG)
    try:
        for char in characters:
            await save_character(conn, char)
        logger.info(f"Загружено {len(characters)} персонажей")
    finally:
        await conn.close()


if __name__ == "__main__":
    start_time = time.time()  
    asyncio.run(main())
    end_time = time.time()
    elapsed_time = end_time - start_time
    print(f"Время выполнения скрипта: {elapsed_time:.2f} секунд")