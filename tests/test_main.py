import json

from fastapi.testclient import TestClient

from main.app import app

client = TestClient(app)

with open("cookbook.json", mode="r", encoding="utf-8") as file:
    cookbook_db = json.load(file)

new_recipe = {
    "name": "Новый рецепт",
    "cooking_time": 10,
    "views_amount": 0,
    "description": "Готовить так-то",
    "cuisine": "Русская",
    "ingredients": [
        {"name": "ингредиент 1", "quantity": "1 шт"},
        {"name": "ингредиент 2", "quantity": "100 г"},
    ],
    "created_at": "2024-10-25T13:08:06.730568",
    "id": 5,
}


def test_get_recipes():
    preview = ["name", "cooking_time", "views_amount"]
    expected_response = [
        {key: value for (key, value) in recipe.items() if key in preview}
        for recipe in cookbook_db
    ]
    response = client.get("/recipes")
    assert response.status_code == 200
    assert response.json() == expected_response


def test_add_recipe():
    response = client.post("/recipes", json=new_recipe)
    assert response.status_code == 200
    assert response.json() == new_recipe


def test_add_recipe_without_name():
    bad_recipe = new_recipe.copy()
    del bad_recipe["name"]
    response = client.post("/recipes", json=bad_recipe)
    assert response.status_code == 422
    assert response.json() == {
        "detail": [
            {
                "type": "missing",
                "loc": ["body", "name"],
                "msg": "Field required",
                "input": bad_recipe,
            }
        ]
    }


def test_add_recipe_without_cooking_time():
    bad_recipe = new_recipe.copy()
    del bad_recipe["cooking_time"]
    response = client.post("/recipes", json=bad_recipe)
    assert response.status_code == 422
    assert response.json() == {
        "detail": [
            {
                "type": "missing",
                "loc": ["body", "cooking_time"],
                "msg": "Field required",
                "input": bad_recipe,
            }
        ]
    }


def test_add_recipe_without_description():
    bad_recipe = new_recipe.copy()
    del bad_recipe["description"]
    response = client.post("/recipes", json=bad_recipe)
    assert response.status_code == 422
    assert response.json() == {
        "detail": [
            {
                "type": "missing",
                "loc": ["body", "description"],
                "msg": "Field required",
                "input": bad_recipe,
            }
        ]
    }


def test_add_recipe_with_wrong_cuisine():
    bad_recipe = new_recipe.copy()
    bad_recipe["cuisine"] = "Немецкая"
    response = client.post("/recipes", json=bad_recipe)
    assert response.status_code == 422
    assert response.json() == {
        "detail": [
            {
                "type": "enum",
                "loc": ["body", "cuisine"],
                "msg": "Input should be 'Русская', 'Китайская', 'Японская', 'Индийская', 'Итальянская', 'Французская', 'Грузинская', 'Паназиатская', 'Мексиканская' or 'Интернациональная'",
                "input": "Немецкая",
                "ctx": {
                    "expected": "'Русская', 'Китайская', 'Японская', 'Индийская', 'Итальянская', 'Французская', 'Грузинская', 'Паназиатская', 'Мексиканская' or 'Интернациональная'"
                },
            }
        ]
    }


def test_get_recipe_by_id():
    new_recipe["views_amount"] += 1
    response = client.get(f"/recipes/{new_recipe['id']}")
    assert response.status_code == 200
    assert response.json() == new_recipe


def test_delete_recipe_by_id():
    response = client.delete(f"/recipes/{new_recipe['id']}")
    assert response.status_code == 200
    assert response.json() == {"message": "Recipe deleted"}


def test_get_nonexistent_recipe():
    response = client.get(f"/recipes/{new_recipe['id']}")
    assert response.status_code == 404
    assert response.json() == {"detail": "Recipe not found"}
