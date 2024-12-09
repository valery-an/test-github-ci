from contextlib import asynccontextmanager
from typing import List

from fastapi import HTTPException, FastAPI
from sqlalchemy.future import select
from sqlalchemy.orm import selectinload

import models
import schemas
from database import engine, session


@asynccontextmanager
async def lifespan(app: FastAPI):
    async with engine.begin() as conn:
        await conn.run_sync(models.Base.metadata.create_all)
    yield
    await session.close()
    await engine.dispose()


app = FastAPI(lifespan=lifespan)


@app.get("/recipes", response_model=List[schemas.RecipeSchemaPreview], tags=['recipes'])
async def get_recipes() -> List[models.Recipe]:
    """Получить список всех рецептов"""
    async with session.begin():
        result = await session.execute(select(models.Recipe))
    return result.scalars().all()


@app.post("/recipes", response_model=schemas.RecipeSchemaOut, tags=["recipes"])
async def add_recipe(recipe: schemas.RecipeSchemaIn) -> models.Recipe:
    """Добавить новый рецепт в БД"""
    new_recipe = models.Recipe(**recipe.model_dump(exclude={"ingredients"}))
    for ingredient in recipe.ingredients:
        new_ingredient = models.Ingredient(**ingredient.model_dump())
        new_recipe.ingredients.append(new_ingredient)
    async with session.begin():
        session.add(new_recipe)
        await session.commit()
    return new_recipe


@app.get(
    "/recipes/{recipe_id}", response_model=schemas.RecipeSchemaOut, tags=["recipes"]
)
async def get_recipe_by_id(recipe_id: int) -> models.Recipe:
    """Получить детальную информацию о рецепте"""
    async with session.begin():
        query = (
            select(models.Recipe)
            .filter_by(id=recipe_id)
            .options(selectinload(models.Recipe.ingredients))
        )
        result = await session.execute(query)
        recipe = result.scalar_one_or_none()
        if not recipe:
            raise HTTPException(status_code=404, detail="Recipe not found")
        recipe.views_amount += 1
        await session.commit()
    return recipe


@app.delete("/recipes/{recipe_id}", tags=["recipes"])
async def delete_recipe_by_id(recipe_id: int):
    """Удалить информацию о рецепте"""
    async with session.begin():
        recipe = await session.get(models.Recipe, recipe_id)
        if not recipe:
            raise HTTPException(status_code=404, detail="Recipe not found")
        await session.delete(recipe)
        await session.commit()
    return {"message": "Recipe deleted"}
