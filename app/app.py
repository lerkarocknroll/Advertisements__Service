from fastapi import FastAPI, Depends, Query
from typing import Annotated, Optional
from sqlalchemy.ext.asyncio import AsyncSession

from app.lifespan import lifespan
from app import models, schemas
from app.dependencies import get_db_session
from app.services import add_item, get_item, update_item, delete_item, get_advertisements

app = FastAPI(
    title="Advertisements Service",
    description="Service for buying/selling advertisements",
    version="0.1.0",
    lifespan=lifespan
)

SessionDep = Annotated[AsyncSession, Depends(get_db_session)]


@app.post("/advertisement", response_model=schemas.AdvertisementResponse)
async def create_advertisement(
    ad_data: schemas.AdvertisementCreate,
    session: SessionDep
):
    # Создать новое объявление
    new_ad = await add_item(session, models.Advertisement, ad_data)
    return new_ad


@app.get("/advertisement/{ad_id}", response_model=schemas.AdvertisementResponse)
async def get_advertisement(
    ad_id: int,
    session: SessionDep
):
    # Получить объявление по ID
    ad = await get_item(session, models.Advertisement, ad_id)
    return ad


@app.patch("/advertisement/{ad_id}", response_model=schemas.AdvertisementResponse)
async def update_advertisement(
    ad_id: int,
    ad_update: schemas.AdvertisementUpdate,
    session: SessionDep
):
    # Обновить объявление
    updated_ad = await update_item(session, models.Advertisement, ad_id, ad_update)
    return updated_ad


@app.delete("/advertisement/{ad_id}", response_model=schemas.OKResponse)
async def delete_advertisement(
    ad_id: int,
    session: SessionDep
):
    #Удалить объявление
    await delete_item(session, models.Advertisement, ad_id)
    return schemas.OKResponse()


@app.get("/advertisement", response_model=list[schemas.AdvertisementResponse])
async def search_advertisements(
    session: SessionDep,  # <-- ПЕРЕНЕСЕНО В НАЧАЛО
    title: Optional[str] = Query(None, description="Фильтр по заголовку (содержит)"),
    description: Optional[str] = Query(None, description="Фильтр по описанию (содержит)"),
    author: Optional[str] = Query(None, description="Фильтр по автору (содержит)"),
    price_min: Optional[float] = Query(None, ge=0, description="Минимальная цена"),
    price_max: Optional[float] = Query(None, ge=0, description="Максимальная цена"),
    skip: int = Query(0, ge=0, description="Сколько пропустить"),
    limit: int = Query(100, ge=1, le=1000, description="Размер страницы")
):
    # Поиск объявлений по различным критериям.
    ads = await get_advertisements(
        session,
        title=title,
        description=description,
        author=author,
        price_min=price_min,
        price_max=price_max,
        skip=skip,
        limit=limit
    )
    return ads