import asyncio
import datetime
from itertools import batched

import aiohttp

from db import DbSession, SwapiPeople, close_orm, init_orm

MAX_REQUESTS = 10


async def get_people(person_id: int, session: aiohttp.ClientSession):
    response = await session.get(f"https://swapi.py4e.com/api/people/{person_id}/")
    json_data = await response.json()
    return json_data


async def insert_peoples(people_list: list[dict]):
    async with DbSession() as session:
        people_orm = [SwapiPeople(json=item) for item in people_list]
        session.add_all(people_orm)
        await session.commit()


async def main():
    await init_orm()
    async with aiohttp.ClientSession() as http_session:
        for people_id_batch in batched(range(1, 101), MAX_REQUESTS):
            coros = [get_people(i, http_session) for i in people_id_batch]
            # for i in people_id_batch:
            #     coro = get_people(i)
            #     coros.append(coro)
            result = await asyncio.gather(*coros)
            insert_task = asyncio.create_task(insert_peoples(people_list=result))
    tasks = asyncio.all_tasks()
    main_task = asyncio.current_task()
    tasks.remove(main_task)
    for task in tasks:
        await task
    await close_orm()


start = datetime.datetime.now()
asyncio.run(main())
print(datetime.datetime.now() - start)
