from fastapi import FastAPI
import asyncio
import aiosqlite
import os

# Создаем директорию для данных, если её нет
os.makedirs("./data", exist_ok=True)

app = FastAPI(title="Service d'annonces", version="1.0.0")

# Импорт маршрутов с использованием относительного импорта
from .routers.advertisements import router as advertisements_router

app.include_router(advertisements_router)

@app.on_event("startup")
async def startup():
    async with aiosqlite.connect("./data/advertisements.db") as db:
        await db.execute('''
            CREATE TABLE IF NOT EXISTS advertisements (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                title TEXT NOT NULL,
                description TEXT,
                price REAL NOT NULL,
                author TEXT NOT NULL,
                created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
            )
        ''')
        await db.commit()

@app.get("/")
def read_root():
    return {"message": "Service d'annonces API"}