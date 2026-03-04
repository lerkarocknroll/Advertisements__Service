from fastapi import HTTPException, status
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select
from app import models
from typing import Optional, List

async def add_item(
    session: AsyncSession,
    orm_model: type,
    item_data
):
    # функция для добавления записи
    new_item = orm_model(**item_data.model_dump())
    session.add(new_item)
    await session.commit()
    await session.refresh(new_item)
    return new_item

async def get_item(
    session: AsyncSession,
    orm_model: type,
    item_id: int
):
    # Получить запись по ID или 404
    stmt = select(orm_model).where(orm_model.id == item_id)
    result = await session.execute(stmt)
    item = result.scalar_one_or_none()
    if not item:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"{orm_model.__name__} with id {item_id} not found"
        )
    return item

async def update_item(
    session: AsyncSession,
    orm_model: type,
    item_id: int,
    update_data
):
    # Обновить запись: только переданные поля
    item = await get_item(session, orm_model, item_id)
    update_dict = update_data.model_dump(exclude_unset=True)
    for key, value in update_dict.items():
        setattr(item, key, value)
    await session.commit()
    await session.refresh(item)
    return item

async def delete_item(
    session: AsyncSession,
    orm_model: type,
    item_id: int
) -> None:
    # Удалить запись
    item = await get_item(session, orm_model, item_id)
    await session.delete(item)
    await session.commit()

async def get_advertisements(
    session: AsyncSession,
    title: Optional[str] = None,
    description: Optional[str] = None,
    author: Optional[str] = None,
    price_min: Optional[float] = None,
    price_max: Optional[float] = None,
    skip: int = 0,
    limit: int = 100
) -> List[models.Advertisement]:
    # Поиск объявлений с фильтрацией
    query = select(models.Advertisement)
    if title:
        query = query.where(models.Advertisement.title.contains(title))
    if description:
        query = query.where(models.Advertisement.description.contains(description))
    if author:
        query = query.where(models.Advertisement.author.contains(author))
    if price_min is not None:
        query = query.where(models.Advertisement.price >= price_min)
    if price_max is not None:
        query = query.where(models.Advertisement.price <= price_max)
    query = query.offset(skip).limit(limit)
    result = await session.execute(query)
    return result.scalars().all()