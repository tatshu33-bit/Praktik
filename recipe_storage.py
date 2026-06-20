"""
recipe_storage.py

Модуль відповідає за зберігання та обробку даних бібліотеки рецептів.
Дані зберігаються у JSON-файлі, щоб були доступні між сесіями запуску утиліти.
"""

import json
import os

DATA_FILE = "recipes.json"


def load_recipes(filepath=DATA_FILE):
    """
    Завантажує список рецептів з JSON-файлу.
    Якщо файл відсутній, пошкоджений або порожній — повертає порожній список,
    не аварійно завершуючи роботу програми.
    """
    if not os.path.exists(filepath):
        return []

    try:
        with open(filepath, "r", encoding="utf-8") as f:
            content = f.read().strip()
            if not content:
                return []
            data = json.loads(content)
            if not isinstance(data, list):
                print("Попередження: файл даних мав неочікуваний формат. "
                      "Розпочинаємо з порожньої бібліотеки.")
                return []
            return data
    except (json.JSONDecodeError, OSError) as e:
        print(f"Попередження: не вдалося прочитати файл даних ({e}). "
              f"Розпочинаємо з порожньої бібліотеки.")
        return []


def save_recipes(recipes, filepath=DATA_FILE):
    """
    Зберігає список рецептів у JSON-файл.
    Повертає True у разі успіху, False — якщо сталася помилка запису.
    """
    try:
        with open(filepath, "w", encoding="utf-8") as f:
            json.dump(recipes, f, ensure_ascii=False, indent=2)
        return True
    except OSError as e:
        print(f"Помилка: не вдалося зберегти дані ({e}).")
        return False


def add_recipe(recipes, name, ingredients, time_minutes):
    """
    Додає новий рецепт до списку.
    ingredients очікується як список рядків (назв інгредієнтів).
    time_minutes — час приготування у хвилинах (ціле додатне число).
    Повертає оновлений список рецептів.
    """
    recipe = {
        "name": name.strip(),
        "ingredients": [i.strip() for i in ingredients if i.strip()],
        "time_minutes": time_minutes,
    }
    recipes.append(recipe)
    return recipes


def find_by_name(recipes, query):
    """
    Шукає рецепти, назва яких містить підрядок query (без урахування регістру).
    Повертає список знайдених рецептів.
    """
    query_lower = query.strip().lower()
    return [r for r in recipes if query_lower in r["name"].lower()]


def find_by_ingredient(recipes, query):
    """
    Шукає рецепти, що містять інгредієнт, у назві якого є підрядок query
    (без урахування регістру).
    Повертає список знайдених рецептів.
    """
    query_lower = query.strip().lower()
    result = []
    for r in recipes:
        for ingredient in r["ingredients"]:
            if query_lower in ingredient.lower():
                result.append(r)
                break
    return result


def delete_recipe(recipes, index):
    """
    Видаляє рецепт за індексом (0-based) зі списку.
    Повертає кортеж (оновлений_список, видалений_рецепт_або_None).
    """
    if 0 <= index < len(recipes):
        removed = recipes.pop(index)
        return recipes, removed
    return recipes, None
