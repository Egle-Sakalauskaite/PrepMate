"""This file contains the unit tests for all the database functions."""

# Imports for this file
import unittest

# Imports from this project
from project.back_end.database import Database
from project.back_end.ingredient import Ingredient
from project.back_end.recipe import Recipe
from project.back_end.user import User


class TestDatabase(unittest.TestCase):
    """This class contains all the unit tests related to the database."""
    def init_db(self) -> Database:
        """Initialize the database."""
        db_filename = 'test_database.db'
        db = Database(db_filename)
        db.csv_to_database('csv_files/ingredients.csv')
        return db

    def test_init_db(self):
        """Test if the database is initialized correctly."""
        db = self.init_db()
        self.assertIsNotNone(db)
        self.assertIsNotNone(db.conn)
        self.assertIsNotNone(db.cursor)

    def test_add_and_retrieve_user_allergies(self) -> None:
        """Test if the user allergies are added and retrieved correctly."""
        db = self.init_db()
        db.create_table_allergies()
        db.create_table_dietary_restrictions()
        allergies = {'soy'}
        user = User(allergies=allergies)
        db.add_user_info(user)
        retrieved_user = db.retrieve_user_info()
        self.assertEqual(user.allergies, retrieved_user.allergies)

    def test_add_and_retrieve_user_dietary_restrictions(self) -> None:
        """Test if the user dietary_restrictions are added and retrieved correctly."""
        db = self.init_db()
        db.create_table_allergies()
        db.create_table_dietary_restrictions()
        user = User(is_vegetarian=True)
        db.add_user_info(user)
        retrieved_user = db.retrieve_user_info()
        self.assertFalse(retrieved_user.is_vegan)
        self.assertTrue(retrieved_user.is_vegetarian)
        self.assertFalse(retrieved_user.is_lactose_intolerant)

    def test_add_same_ingredient_same_unit_to_the_shopping_list(self) -> None:
        """Test if the ingredients are added and retrieved correctly from shopping list
        when the name and units match."""
        db = self.init_db()
        db.create_table_shopping_list()
        db.cursor.execute('DELETE FROM shopping_list')
        ingredient_1 = Ingredient('Onion', quantity=1, unit='piece')
        ingredient_2 = Ingredient('Onion', quantity=2, unit='piece')
        db.add_ingredient_to_shopping_list(ingredient_1)
        db.add_ingredient_to_shopping_list(ingredient_2)
        shopping_list = db.retrieve_shopping_list()
        self.assertEqual(shopping_list[0].name, 'Onion')
        self.assertEqual(shopping_list[0].quantity, 3)
        self.assertEqual(shopping_list[0].unit, 'piece')

    def test_add_same_ingredient_different_unit_to_the_shopping_list(self) -> None:
        """Test if the ingredients are added and retrieved correctly from shopping list
        when only the name matches."""
        db = self.init_db()
        db.create_table_shopping_list()
        db.cursor.execute('DELETE FROM shopping_list')
        ingredient_1 = Ingredient('Chicken', quantity=200, unit='g')
        ingredient_2 = Ingredient('Chicken', quantity=1, unit='piece')
        db.add_ingredient_to_shopping_list(ingredient_1)
        db.add_ingredient_to_shopping_list(ingredient_2)
        shopping_list = db.retrieve_shopping_list()
        self.assertEqual(shopping_list[0].quantity, 200)
        self.assertEqual(shopping_list[0].unit, 'g')
        self.assertEqual(shopping_list[1].quantity, 1)
        self.assertEqual(shopping_list[1].unit, 'piece')

    def test_add_and_retrieve_recipe(self) -> None:
        """Test if the recipe is added and retrieved correctly."""
        db = self.init_db()
        db.create_table_recipes()
        db.create_table_ingredients()
        db.cursor.execute('DELETE FROM recipes')
        db.cursor.execute('DELETE FROM ingredients')
        ingredient_1 = Ingredient('Onion', quantity=1, unit='piece')
        ingredient_2 = Ingredient('Chicken', quantity=200, unit='g')
        ingredient_3 = Ingredient('Potato', quantity=75, unit='g')
        ingredients = [ingredient_1, ingredient_2, ingredient_3]
        recipe = Recipe('Chicken and Rice', calories=400, prep_time=25, ingredients=ingredients)
        db.add_recipe(recipe)
        retrieved_recipes = db.retrieve_recipes()
        retrieved_recipe = retrieved_recipes[0]
        self.assertEqual(recipe.prep_time, retrieved_recipe.prep_time)
        self.assertEqual(len(recipe.ingredients), len(retrieved_recipe.ingredients))
        self.assertEqual(recipe.ingredients[1].name, retrieved_recipe.ingredients[1].name)
        self.assertEqual(True, retrieved_recipe.ingredients[2].is_vegan)

    def test_add_and_retrieve_new_ingredient_info(self):
        """Test if the new ingredient info is added and retrieved correctly."""
        db = self.init_db()
        ingredient_name = 'new ingredient'
        ingredient_info = {'is_vegan': True, 'is_vegetarian': False, 'is_lactose_free': True}
        db.add_new_ingredient_info(ingredient_name, ingredient_info)
        retrieved_ingredient_info = db.get_ingredient_info(ingredient_name)
        self.assertEqual(ingredient_info, retrieved_ingredient_info)

    def test_add_and_retrieve_meal_plans(self):
        """Test if the planned meals are added and retrieved correctly."""
        db = self.init_db()
        db.create_table_meal_plans()
        ingredient_1 = Ingredient('Fish', quantity=1, unit='piece')
        ingredient_2 = Ingredient('Fries', quantity=200, unit='g')
        ingredients = [ingredient_1, ingredient_2]
        recipe = Recipe('Fish and Chips', calories=650, prep_time=20, ingredients=ingredients)
        date = "29-01-2024"
        db.add_planned_meal(date, recipe.name)
        retrieved_planned_meal = db.retrieve_planned_meal(date)
        self.assertEqual(recipe.name, retrieved_planned_meal)
        date_dummy = "21-01-2024"
        self.assertEqual(db.retrieve_planned_meal(date_dummy), "")


if __name__ == '__main__':
    unittest.main()
