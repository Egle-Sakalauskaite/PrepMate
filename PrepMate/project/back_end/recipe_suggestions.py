"""
This module will be used to generate random recipe suggestions. It will also be used 
to filter the recipes based on the user preferences.
"""

# Imports for this class
import random as rnd

# Imports from this project
from project.back_end.user import User
from project.back_end.database import Database
from project.back_end.recipe import Recipe


class Suggestions():
    """This class will be used to generate recipe suggestions based on the user preferences"""
    def __init__(self, user=None, recipes=None) -> None:
        self.user: User = user or Database('PrepMate.db').retrieve_user_info()
        self.all_recipes: list[Recipe] = recipes or Database('PrepMate.db').retrieve_recipes()
        self.filtered_recipes: list[Recipe] | None = self.check_user_information(self.all_recipes)
        self.suggestions: list[Recipe] = []

    def random_suggestions(self) -> None:
        """This method will generate a list of random recipes"""
        random_recipes = []
        if self.filtered_recipes is not None:
            if self.suggestions == [] and len(self.filtered_recipes) > 10:
                random_recipes = rnd.sample(self.filtered_recipes, 10)
            elif self.suggestions == [] and len(self.filtered_recipes) < 10:
                random_recipes = rnd.sample(self.filtered_recipes, len(self.filtered_recipes))
            else:
                recipes = [
                    recipe for recipe in self.filtered_recipes if recipe not in self.suggestions
                    ]
                if len(recipes) > 10:
                    random_recipes = rnd.sample(recipes, 10)
                else:
                    random_recipes = rnd.sample(recipes, len(recipes))

        self.suggestions = random_recipes

    def check_user_information(self, recipes: list[Recipe]) -> list[Recipe]:
        """
        This method will be used as filter for the recipes
        """
        filtered_recipes = []
        for recipe in recipes:
            # Vegan
            if self.user.is_vegan:
                if recipe.is_vegan:
                    filtered_recipes.append(recipe)
            # Vegetarian
            elif self.user.is_vegetarian:
                if recipe.is_vegetarian:
                    filtered_recipes.append(recipe)
            # Lactose intolerant
            elif self.user.is_lactose_intolerant:
                if recipe.is_lactose_free:
                    filtered_recipes.append(recipe)
            else:
                filtered_recipes.append(recipe)

        # Pop recipes that contain allergens
        if len(self.user.allergies) > 0:
            for allergen in self.user.allergies:
                for recipe in filtered_recipes.copy():
                    if recipe.contains(allergen):
                        filtered_recipes.remove(recipe)

        return filtered_recipes

    def check_user_preferences(
            self,
            must_haves: list[str],
            should_not_haves: list[str],
            calorie_min_max: tuple[int, int] | None,
            max_time: int | None
            ) -> None:
        """
        This method will be used to check the user preferences, it will be used in the front end.
        """
        if self.filtered_recipes is not None:
            preferences_recipes = []
            for recipe in self.filtered_recipes:
                # Check the cooking time
                if max_time is not None and recipe.prep_time is not None:
                    if recipe.prep_time > max_time:
                        continue

                # Check the calories
                if calorie_min_max is not None and recipe.calories is not None:
                    if recipe.calories < calorie_min_max[0] or recipe.calories > calorie_min_max[1]:
                        continue

                # Check the must haves
                recipe_ingredients_names = [ingredient.name for ingredient in recipe.ingredients]
                if any(ingredient not in recipe_ingredients_names for ingredient in must_haves):
                    continue

                # Check the should not haves
                if any(ingredient in recipe_ingredients_names for ingredient in should_not_haves):
                    continue

                # If all conditions are met, add the recipe to the preferences_recipes list
                preferences_recipes.append(recipe)

            # Change the filtered recipes to the preferences recipes
            self.filtered_recipes = preferences_recipes
