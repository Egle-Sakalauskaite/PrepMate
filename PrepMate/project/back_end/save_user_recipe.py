"""This module contains the functions to
add a user's own recipe to the database"""


import os
import string
from typing import Any
from project.back_end.ingredient import Ingredient
from project.back_end.recipe import Recipe
from project.back_end.database import Database


def save_user_recipe(
        user_recipe: tuple[str, int, int, list[list[int | bool | Any]], list[str]],
        database_file: str = 'PrepMate.db'
) -> None | int:
    """Adds the user's recipe to the database but returns an integer
    if an error occurs. Default database file used is 'PrepMate.db'"""
    title = user_recipe[0]
    calories = user_recipe[1]
    prep_time = user_recipe[2]
    ingredients = user_recipe[3]
    instructions = user_recipe[4]

    # Checking whether the recipe has a name
    if len(title) == 0:
        return 0

    # Making sure the title is valid
    for letter in title:
        if letter not in string.ascii_letters + string.digits + " -,":
            return 3

    # Initializing the database
    db: Database = Database(database_file)

    # Checking whether the recipe doesn't exist already
    existing_recipes: list[Recipe] = db.retrieve_recipes()
    if title.lower() in (existing.name.lower() for existing in existing_recipes):
        return 1

    # Making sure the ingredient data is right and the ingredients have a unit
    for ingredient in ingredients:
        if ingredient[2] == '':
            return 4
        for i in range(3, 6):
            if ingredient[i]:
                ingredient[i] = True
            else:
                ingredient[i] = False

    # Saving the ingredients as a list of Ingredient objects
    ingredient_list: list[Ingredient] = []
    for ingredient in ingredients:
        ingredient_list.append(
            Ingredient(
                name=str(ingredient[0]),
                quantity=ingredient[1],
                unit=ingredient[2],
                is_vegan=ingredient[3],
                is_vegetation=ingredient[4],
                is_lactose_free=ingredient[5]
            )
        )
        # Adding the ingredients info to the database
        db.add_new_ingredient_info(
            ingredient[0],
            {
                "is_vegan": bool(ingredient[3]),
                "is_vegetarian": bool(ingredient[4]),
                "is_lactose_free": bool(ingredient[5])
            }
        )

    # Checking whether the recipe has at least one ingredient
    if len(ingredient_list) < 1:
        return 2

    # Creating a text file for the instructions, if provided
    if len(instructions) > 0:
        create_instructions_file(title, instructions)

    # Creating a Recipe object for the user's recipe and adding it to the database
    recipe = Recipe(
        name=title,
        ingredients=ingredient_list,
        prep_time=prep_time,
        calories=calories
    )
    db.add_recipe(recipe)
    return None


def create_instructions_file(title: str, instructions: list[str]) -> None:
    """Creates a text file containing
    the provided instructions"""
    project_folder: str = os.path.dirname(__file__)
    file_name: str = str(title) + '.txt'
    file_path: str = os.path.abspath(os.path.join(project_folder, 'instructions_files', file_name))
    with open(file_path, "w", encoding="utf-8") as f:
        for line in instructions:
            f.write(line + "\n")
