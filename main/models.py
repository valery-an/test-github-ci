from datetime import datetime

from sqlalchemy import Column, DateTime, ForeignKey, Integer, SmallInteger, String
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import relationship

Base = declarative_base()


class Ingredient(Base):  # type: ignore
    """Модель ингредиента"""

    __tablename__ = "ingredients"
    id = Column(Integer, primary_key=True)
    name = Column(String(100), nullable=False)
    quantity = Column(String(20), nullable=False)
    recipe_id = Column(Integer, ForeignKey("recipes.id"), nullable=False)

    recipe = relationship("Recipe", back_populates="ingredients")


class Recipe(Base):  # type: ignore
    """Модель рецепта"""

    __tablename__ = "recipes"
    id = Column(Integer, primary_key=True)
    name = Column(String(100), nullable=False)
    cuisine = Column(String(40))
    description = Column(String(1000), nullable=False)
    cooking_time = Column(SmallInteger, nullable=False)
    created_at = Column(DateTime, default=datetime.now())
    views_amount = Column(Integer, default=0)

    ingredients = relationship(
        "Ingredient", back_populates="recipe", cascade="all,delete"
    )
