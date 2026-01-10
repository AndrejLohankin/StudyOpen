from fastapi import APIRouter, Depends, HTTPException, Query
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import text
from typing import List, Optional
from ..database import get_async_db
from ..models import Advertisement as AdvertisementModel
from ..schemas import Advertisement, AdvertisementCreate, AdvertisementUpdate

router = APIRouter(prefix="/advertisement", tags=["advertisements"])


@router.post("/", response_model=Advertisement)
async def create_advertisement(advertisement: AdvertisementCreate, db: AsyncSession = Depends(get_async_db)):
    # Создаем объект модели
    db_advertisement = AdvertisementModel(
        title=advertisement.title,
        description=advertisement.description,
        price=advertisement.price,
        author=advertisement.author
    )

    # Добавляем в сессию
    db.add(db_advertisement)
    await db.commit()
    await db.refresh(db_advertisement)

    # Преобразуем в Pydantic модель для ответа
    return Advertisement(
        id=db_advertisement.id,
        title=db_advertisement.title,
        description=db_advertisement.description,
        price=db_advertisement.price,
        author=db_advertisement.author,
        created_at=db_advertisement.created_at
    )


@router.get("/{advertisement_id}", response_model=Advertisement)
async def get_advertisement(advertisement_id: int, db: AsyncSession = Depends(get_async_db)):
    result = await db.execute(text("SELECT * FROM advertisements WHERE id = :id"), {"id": advertisement_id})
    row = result.fetchone()

    if not row:
        raise HTTPException(status_code=404, detail="Advertisement not found")

    # Преобразуем строку в Pydantic модель
    return Advertisement(
        id=row[0],
        title=row[1],
        description=row[2],
        price=row[3],
        author=row[4],
        created_at=row[5]
    )


@router.patch("/{advertisement_id}", response_model=Advertisement)
async def update_advertisement(
        advertisement_id: int,
        advertisement_update: AdvertisementUpdate,
        db: AsyncSession = Depends(get_async_db)
):
    # Получаем существующее объявление
    result = await db.execute(text("SELECT * FROM advertisements WHERE id = :id"), {"id": advertisement_id})
    row = result.fetchone()

    if not row:
        raise HTTPException(status_code=404, detail="Advertisement not found")

    # Формируем обновленные данные
    updated_data = {
        "title": advertisement_update.title or row[1],
        "description": advertisement_update.description or row[2],
        "price": advertisement_update.price or row[3],
        "author": advertisement_update.author or row[4],
    }

    # Обновляем запись
    await db.execute(
        text("""
            UPDATE advertisements 
            SET title = :title, description = :description, 
                price = :price, author = :author 
            WHERE id = :id
        """),
        {"id": advertisement_id, **updated_data}
    )
    await db.commit()

    # Возвращаем обновленную запись
    result = await db.execute(text("SELECT * FROM advertisements WHERE id = :id"), {"id": advertisement_id})
    updated_row = result.fetchone()

    return Advertisement(
        id=updated_row[0],
        title=updated_row[1],
        description=updated_row[2],
        price=updated_row[3],
        author=updated_row[4],
        created_at=updated_row[5]
    )


@router.delete("/{advertisement_id}")
async def delete_advertisement(advertisement_id: int, db: AsyncSession = Depends(get_async_db)):
    result = await db.execute(text("SELECT * FROM advertisements WHERE id = :id"), {"id": advertisement_id})
    row = result.fetchone()

    if not row:
        raise HTTPException(status_code=404, detail="Advertisement not found")

    await db.execute(text("DELETE FROM advertisements WHERE id = :id"), {"id": advertisement_id})
    await db.commit()

    return {"message": "Advertisement deleted successfully"}


@router.get("/", response_model=List[Advertisement])
async def search_advertisements(
        title: Optional[str] = Query(None),
        author: Optional[str] = Query(None),
        min_price: Optional[float] = Query(None),
        max_price: Optional[float] = Query(None),
        db: AsyncSession = Depends(get_async_db)
):
    # Начинаем формировать SQL запрос
    base_query = "SELECT * FROM advertisements"
    conditions = []
    params = {}

    if title:
        conditions.append("title LIKE :title")
        params["title"] = f"%{title}%"

    if author:
        conditions.append("author LIKE :author")
        params["author"] = f"%{author}%"

    if min_price is not None:
        conditions.append("price >= :min_price")
        params["min_price"] = min_price

    if max_price is not None:
        conditions.append("price <= :max_price")
        params["max_price"] = max_price

    if conditions:
        base_query += " WHERE " + " AND ".join(conditions)

    # Сортировка по дате создания (новые сверху)
    base_query += " ORDER BY created_at DESC"

    result = await db.execute(text(base_query), params)
    rows = result.fetchall()

    # Преобразуем результаты в Pydantic модели
    advertisements = []
    for row in rows:
        advertisements.append(Advertisement(
            id=row[0],
            title=row[1],
            description=row[2],
            price=row[3],
            author=row[4],
            created_at=row[5]
        ))

    return advertisements