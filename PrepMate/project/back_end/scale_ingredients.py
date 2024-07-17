"""This module contains the function to scale ingredients
to a certain amount of servings"""


from project.back_end.ingredient import Ingredient


def scale_ingredients(ingredient_list: list[Ingredient], servings: int) -> list[Ingredient]:
    """Scales the ingredient list to the given amount of servings"""
    new_list = []
    for new_ingredient in ingredient_list.copy():
        if new_ingredient.quantity is not None:
            new_ingredient.quantity = new_ingredient.quantity * servings
        new_list.append(new_ingredient)
    return new_list
