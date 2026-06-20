"""
test_recipe_storage.py

Автоматизований тест для модуля recipe_storage.

Перевіряється повний життєвий цикл рецепту:
  1. Додавання рецепту до списку.
  2. Збереження списку у тимчасовий JSON-файл.
  3. Завантаження списку з файлу (імітація нової сесії програми).
  4. Пошук доданого рецепту за назвою та за інгредієнтом.
  5. Видалення рецепту та перевірка, що він зник зі списку.

Запуск: python test_recipe_storage.py
Очікуваний результат: "УСІ ТЕСТИ ПРОЙШЛИ УСПІШНО".
"""

import os

from recipe_storage import (
    load_recipes,
    save_recipes,
    add_recipe,
    find_by_name,
    find_by_ingredient,
    delete_recipe,
)

TEST_FILE = "test_recipes_temp.json"


def run_test():
    # Прибираємо тестовий файл, якщо залишився з попереднього запуску
    if os.path.exists(TEST_FILE):
        os.remove(TEST_FILE)

    try:
        # 1. Починаємо з порожнього списку (файлу ще не існує)
        recipes = load_recipes(TEST_FILE)
        assert recipes == [], "Очікувався порожній список на старті"

        # 2. Додаємо рецепт
        recipes = add_recipe(
            recipes,
            name="Млинці",
            ingredients=["борошно", "молоко", "яйця"],
            time_minutes=30,
        )
        assert len(recipes) == 1, "Рецепт не додався до списку"

        # 3. Зберігаємо у файл та імітуємо нову сесію - перечитуємо файл
        saved_ok = save_recipes(recipes, TEST_FILE)
        assert saved_ok, "Збереження у файл завершилося невдало"

        reloaded = load_recipes(TEST_FILE)
        assert len(reloaded) == 1, "Дані не збереглися між сесіями"
        assert reloaded[0]["name"] == "Млинці", "Назва рецепту не збереглася коректно"

        # 4a. Пошук за назвою (нечутливий до регістру, частковий збіг)
        found_by_name = find_by_name(reloaded, "млин")
        assert len(found_by_name) == 1, "Пошук за назвою не знайшов рецепт"

        # 4b. Пошук за інгредієнтом
        found_by_ingredient = find_by_ingredient(reloaded, "яйця")
        assert len(found_by_ingredient) == 1, "Пошук за інгредієнтом не знайшов рецепт"

        not_found = find_by_ingredient(reloaded, "шоколад")
        assert len(not_found) == 0, "Пошук за інгредієнтом знайшов зайве"

        # 5. Видалення рецепту
        updated, removed = delete_recipe(reloaded, 0)
        assert removed is not None, "Видалення не повернуло видалений рецепт"
        assert removed["name"] == "Млинці", "Видалено не той рецепт"
        assert len(updated) == 0, "Список після видалення має бути порожнім"

        print("УСІ ТЕСТИ ПРОЙШЛИ УСПІШНО")

    finally:
        # Прибираємо за собою тестовий файл
        if os.path.exists(TEST_FILE):
            os.remove(TEST_FILE)


if __name__ == "__main__":
    run_test()
