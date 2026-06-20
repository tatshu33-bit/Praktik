"""
main.py

Консольна утиліта "Бібліотека рецептів".

Функціональність:
  1. Додавання рецепту (назва, інгредієнти, час приготування)
  2. Пошук рецепту за назвою
  3. Пошук рецепту за інгредієнтом
  4. Перегляд усіх рецептів
  5. Видалення рецепту
  0. Вихід

Дані зберігаються у файлі recipes.json між сесіями запуску програми.
Усі помилки некоректного вводу обробляються без аварійного завершення роботи.
"""

from recipe_storage import (
    load_recipes,
    save_recipes,
    add_recipe,
    find_by_name,
    find_by_ingredient,
    delete_recipe,
)

MENU_TEXT = """
========== БІБЛІОТЕКА РЕЦЕПТІВ ==========
1. Додати рецепт
2. Пошук за назвою
3. Пошук за інгредієнтом
4. Переглянути всі рецепти
5. Видалити рецепт
0. Вихід
==========================================
"""


def print_recipe(recipe, index=None):
    """Виводить інформацію про один рецепт у зручному форматі."""
    prefix = f"[{index}] " if index is not None else ""
    print(f"\n{prefix}Назва: {recipe['name']}")
    print(f"   Час приготування: {recipe['time_minutes']} хв")
    if recipe["ingredients"]:
        print(f"   Інгредієнти: {', '.join(recipe['ingredients'])}")
    else:
        print("   Інгредієнти: не вказано")


def print_recipe_list(recipes):
    """Виводить список рецептів. Якщо список порожній — повідомляє про це."""
    if not recipes:
        print("\nРецептів не знайдено.")
        return
    for idx, r in enumerate(recipes):
        print_recipe(r, idx)


def prompt_non_empty(prompt_text):
    """
    Запитує у користувача непорожній рядок.
    Повторює запит, доки не отримає коректне значення.
    """
    while True:
        value = input(prompt_text).strip()
        if value:
            return value
        print("Поле не може бути порожнім. Спробуйте ще раз.")


def prompt_positive_int(prompt_text):
    """
    Запитує у користувача додатне ціле число.
    Повторює запит при некоректному вводі (нечислове значення, від'ємне число тощо),
    не завершуючи програму аварійно.
    """
    while True:
        raw = input(prompt_text).strip()
        try:
            value = int(raw)
            if value <= 0:
                print("Число має бути більшим за нуль. Спробуйте ще раз.")
                continue
            return value
        except ValueError:
            print("Будь ласка, введіть ціле число (наприклад, 30).")


def handle_add(recipes):
    print("\n--- Додавання нового рецепту ---")
    name = prompt_non_empty("Назва рецепту: ")
    ingredients_raw = input("Інгредієнти (через кому): ").strip()
    ingredients = [i.strip() for i in ingredients_raw.split(",") if i.strip()]
    if not ingredients:
        print("Інгредієнти не вказані, рецепт буде збережено без них.")
    time_minutes = prompt_positive_int("Час приготування (у хвилинах): ")

    add_recipe(recipes, name, ingredients, time_minutes)
    if save_recipes(recipes):
        print(f"Рецепт '{name}' успішно додано та збережено.")
    else:
        print("Рецепт додано до поточної сесії, але виникла помилка збереження у файл.")


def handle_search_by_name(recipes):
    print("\n--- Пошук за назвою ---")
    query = prompt_non_empty("Введіть назву або частину назви: ")
    results = find_by_name(recipes, query)
    print(f"\nЗнайдено рецептів: {len(results)}")
    print_recipe_list(results)


def handle_search_by_ingredient(recipes):
    print("\n--- Пошук за інгредієнтом ---")
    query = prompt_non_empty("Введіть назву інгредієнта або його частину: ")
    results = find_by_ingredient(recipes, query)
    print(f"\nЗнайдено рецептів: {len(results)}")
    print_recipe_list(results)


def handle_view_all(recipes):
    print("\n--- Усі рецепти ---")
    print(f"Усього рецептів: {len(recipes)}")
    print_recipe_list(recipes)


def handle_delete(recipes):
    print("\n--- Видалення рецепту ---")
    if not recipes:
        print("Бібліотека порожня, видаляти нічого.")
        return

    print_recipe_list(recipes)
    raw = input("\nВведіть номер рецепту для видалення (у квадратних дужках) "
                "або 0 для скасування: ").strip()
    try:
        index = int(raw)
    except ValueError:
        print("Некоректне значення, видалення скасовано.")
        return

    if index == 0:
        print("Видалення скасовано.")
        return

    recipes, removed = delete_recipe(recipes, index)
    if removed is None:
        print("Рецепт з таким номером не знайдено.")
        return

    if save_recipes(recipes):
        print(f"Рецепт '{removed['name']}' видалено та зміни збережено.")
    else:
        print(f"Рецепт '{removed['name']}' видалено з поточної сесії, "
              f"але виникла помилка збереження у файл.")


def main():
    recipes = load_recipes()
    print("Ласкаво просимо до утиліти 'Бібліотека рецептів'!")

    while True:
        print(MENU_TEXT)
        choice = input("Оберіть пункт меню: ").strip()

        if choice == "1":
            handle_add(recipes)
        elif choice == "2":
            handle_search_by_name(recipes)
        elif choice == "3":
            handle_search_by_ingredient(recipes)
        elif choice == "4":
            handle_view_all(recipes)
        elif choice == "5":
            handle_delete(recipes)
        elif choice == "0":
            print("До побачення!")
            break
        else:
            print("Невірний пункт меню. Будь ласка, оберіть число від 0 до 5.")


if __name__ == "__main__":
    try:
        main()
    except KeyboardInterrupt:
        print("\n\nРоботу програми перервано користувачем. До побачення!")
