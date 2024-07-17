"""This module tests functions in the save_user_recipe module."""


import unittest
import os
import pathlib as pl
from project.back_end.database import Database
from project.back_end.save_user_recipe import save_user_recipe, create_instructions_file
from project.back_end.recipe import Recipe
from project.back_end.ingredient import Ingredient


class TestSaveUserRecipe(unittest.TestCase):
    """This class contains all the unit tests related to the database."""
    def init_db(self) -> Database:
        """Initialize the database."""
        db_filename: str = 'test_database_save_user_recipe.db'
        db: Database = Database(db_filename)
        db.csv_to_database('csv_files/ingredients.csv')
        db.create_table_recipes()
        db.create_table_ingredients()
        db.cursor.execute('DELETE FROM recipes')
        db.cursor.execute('DELETE FROM ingredients')
        ingredient_1: Ingredient = Ingredient('Onion', quantity=1, unit='piece')
        ingredient_2: Ingredient = Ingredient('Chicken', quantity=200, unit='g')
        ingredient_3: Ingredient = Ingredient('Potato', quantity=75, unit='g')
        ingredients: list[Ingredient] = [ingredient_1, ingredient_2, ingredient_3]
        recipe: Recipe = Recipe(
            'Chicken and Rice',
            calories=400, prep_time=25,
            ingredients=ingredients
        )
        db.add_recipe(recipe)
        return db

    def init_test_values(self) -> list[object]:
        """Initialize the values to be used in tests."""
        db = self.init_db()
        test_values = [
            'test-recipe',
            10,
            200,
            [['ingredient', 100, 'ml', True, True, True]],
            'test_database_save_user_recipe.db',
            db.retrieve_recipes()
        ]
        return test_values

    def test_init_db(self) -> None:
        """Test if the database
        is initialized correctly."""
        db_test = self.init_db()
        self.assertIsNotNone(db_test)
        self.assertIsNotNone(db_test.conn)
        self.assertIsNotNone(db_test.cursor)

    def test_user_recipe_no_title(self):
        """Test if the save_user_recipe method recognizes
        there is no title provided."""
        db = self.init_db()
        test_val = self.init_test_values()
        sur = save_user_recipe((
            '',
            test_val[1],
            test_val[2],
            test_val[3],
            []),
            test_val[4]
        )
        self.assertEqual(sur, 0)
        self.assertEqual(len(test_val[5]), len(db.retrieve_recipes()))

    def test_user_recipe_no_ingredients(self):
        """Test if the save_user_recipe method recognizes
        there are no ingredients provided."""
        db = self.init_db()
        test_val = self.init_test_values()
        sur = save_user_recipe((
            test_val[0],
            test_val[1],
            test_val[2],
            [],
            []),
            test_val[4]
        )
        self.assertEqual(sur, 2)
        self.assertEqual(len(test_val[5]), len(db.retrieve_recipes()))

    def test_user_recipe_successful(self):
        """Test if the save_user_recipe method uploaded the
        recipe to the database successfully."""
        db = self.init_db()
        test_val = self.init_test_values()
        sur = save_user_recipe((
            test_val[0],
            test_val[1],
            test_val[2],
            test_val[3],
            []),
            test_val[4]
        )
        self.assertEqual(sur, None)
        self.assertEqual(len(test_val[5]) + 1, len(db.retrieve_recipes()))
        self.assertEqual(test_val[0], db.retrieve_recipes()[-1].name)

    def test_user_recipe_duplicate(self):
        """Test if the save_user_recipe method recognizes
        a recipe with the same name already exists."""
        db = self.init_db()
        test_val = self.init_test_values()
        sur1 = save_user_recipe((
            test_val[0],
            test_val[1],
            test_val[2],
            test_val[3],
            []),
            test_val[4]
        )
        sur2 = save_user_recipe((
            test_val[0],
            test_val[1],
            test_val[2],
            test_val[3],
            []),
            test_val[4]
        )
        self.assertEqual(sur1, None)
        self.assertEqual(sur2, 1)
        self.assertEqual(len(test_val[5]) + 1, len(db.retrieve_recipes()))

    def test_user_recipe_invalid_title(self):
        """Test if the save_user_recipe method recognizes
        there is no title provided."""
        db = self.init_db()
        test_val = self.init_test_values()
        sur = save_user_recipe((
            '*',
            test_val[1],
            test_val[2],
            test_val[3],
            []),
            test_val[4]
        )
        self.assertEqual(sur, 3)
        self.assertEqual(len(test_val[5]), len(db.retrieve_recipes()))

    def test_user_recipe_no_unit(self):
        """Test if the save_user_recipe method recognizes
        there is no title provided."""
        db = self.init_db()
        test_val = self.init_test_values()
        test_val[3][0][2] = ''
        sur = save_user_recipe((
            test_val[0],
            test_val[1],
            test_val[2],
            test_val[3],
            []),
            test_val[4]
        )
        self.assertEqual(sur, 4)
        self.assertEqual(len(test_val[5]), len(db.retrieve_recipes()))

    def test_create_instructions_file(self) -> None:
        """Test if the instructions file has been created successfully."""
        test_val = self.init_test_values()
        test_instructions: list[str] = ['test_instructions_step1', 'test_instructions_step2']
        create_instructions_file(str(test_val[0]), test_instructions)
        project_folder: str = os.path.dirname(__file__)
        file_name: str = str(test_val[0]) + '.txt'
        file_path: str = os.path.abspath(os.path.join(
            project_folder[0:-4], 'project', 'back_end', 'instructions_files', file_name
        ))
        path = pl.Path(file_path)
        self.assertTrue(path.is_file())
        self.assertTrue(path.parent.is_dir())
        os.remove(file_path)


if __name__ == '__main__':
    unittest.main()
