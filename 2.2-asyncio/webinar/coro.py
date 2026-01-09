import asyncio


async def some_task():
    return print(2 + 2)


async def main():
    coro = some_task()
    resutl = await coro
    coro = some_task()
    result = await asyncio.gather(coro)
    coro = some_task()
    task = asyncio.create_task(coro)


asyncio.run(main())
