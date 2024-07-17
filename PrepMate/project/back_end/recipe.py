"""This module will be used to create recipe objects in the database."""

# Imports from this project
import os
from project.back_end.ingredient import Ingredient


class Recipe:
    """This class will be used to create recipe objects"""
    def __init__(self, name, **kwargs) -> None:
        self.name: str = name
        self.ingredients: list[Ingredient] = kwargs.get('ingredients', [])
        self.calories: int | None = kwargs.get('calories', None)
        self.prep_time: int | None = kwargs.get('prep_time', None)
        self.instructions: list[str] = self.get_instructions_from_file()

    @property
    def is_vegan(self) -> bool:
        """This method will return True if the recipe is vegan, False otherwise"""
        for ingredient in self.ingredients:
            if not ingredient.is_vegan:
                return False

        return True

    @property
    def is_vegetarian(self) -> bool:
        """This method will return True if the recipe is vegetarian, False otherwise"""
        for ingredient in self.ingredients:
            if not ingredient.is_vegetarian:
                return False

        return True

    @property
    def is_lactose_free(self) -> bool:
        """This method will return True if the recipe is lactose free, False otherwise"""
        for ingredient in self.ingredients:
            if not ingredient.is_lactose_free:
                return False

        return True

    def contains(self, allergen: str) -> bool:
        """This method will return True if the recipe contains the allergen, False otherwise"""
        for ingredient in self.ingredients:
            if ingredient.name.lower() == allergen.lower():
                return True

        return False

    def get_instructions_from_file(self) -> list[str]:
        """Returns a list of cooking instructions from a file"""
        project_folder = os.path.dirname(__file__)
        file_name = self.name + '.txt'
        file_path = os.path.abspath(os.path.join(project_folder, 'instructions_files', file_name))
        instructions: list[str] = []

        try:
            with open(file_path, encoding='utf-8') as f:
                for line in f:
                    instructions.append(line)
        except FileNotFoundError:
            print('Instructions not added')

        return instructions
