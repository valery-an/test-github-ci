from datetime import datetime
from enum import Enum
from typing import List, Optional

from pydantic import BaseModel, Field


class Cuisine(str, Enum):
    """ Кухни стран мира """
    russian = 'Русская'
    chinese = 'Китайская'
    japanese = 'Японская'
    indian = 'Индийская'
    italian = 'Итальянская'
    french = 'Французская'
    georgian = 'Грузинская'
    panasian = 'Паназиатская'
    mexican = 'Мексиканская'
    international = 'Интернациональная'


class IngredientSchema(BaseModel):
    """ Модель ингредиента """
    name: str = Field(
        default=...,
        min_length=1,
        max_length=100,
        title='Наименование ингредиента'
    )
    quantity: str = Field(
        default=...,
        min_length=1,
        max_length=20,
        title='Количество'
    )


class RecipeSchemaPreview(BaseModel):
    """ Модель рецепта для предварительного просмотра """
    name: str = Field(
        default=...,
        min_length=1,
        max_length=100,
        title='Название блюда'
    )
    cooking_time: int = Field(
        default=...,
        ge=1,
        le=300,
        title = 'Время приготовления (в минутах)'
    )
    views_amount: int = Field(
        default=0,
        title = 'Количество просмотров'
    )


class RecipeSchemaIn(RecipeSchemaPreview):
    """ Модель рецепта """
    description: str = Field(
        default=...,
        min_length=1,
        max_length=1000,
        title='Описание процесса готовки'
    )
    cuisine: Optional[Cuisine] = Field(
        default=None,
        title='Вид кухни'
    )
    created_at: datetime = Field(
        default=datetime.now(),
        title='Дата публикации'
    )
    ingredients: List[IngredientSchema] = Field(
        default=...,
        title='Список ингредиентов'
    )


class RecipeSchemaOut(RecipeSchemaIn):
    """ Модель рецепта """
    id: int

    class Config:
        from_attributes = True
