"""This module is used for everything related to the database"""

# Imports for this file
import os
import sqlite3
import pandas as pd

# Imports from this project
from project.back_end.recipe import Recipe
from project.back_end.ingredient import Ingredient
from project.back_end.user import User


class Database:
    """This class is used to create SQLite3 database files and manage information stored in them."""
    def __init__(self, filename: str) -> None:
        """Creates a SQLite database if it does not exist and store it in the project folder"""
        self.project_folder = os.path.dirname(__file__)
        self.db_path = os.path.join(self.project_folder, filename)

        self.conn = sqlite3.connect(self.db_path)
        self.cursor = self.conn.cursor()

    def create_table_recipes(self) -> None:
        """creates the recipes table if it doesn't exist already"""
        query = '''
		    CREATE TABLE IF NOT EXISTS recipes (
				id INTEGER PRIMARY KEY AUTOINCREMENT,
		    	name TEXT NOT NULL,
		    	calories INTIGER,
		    	prep_time INTEGER
			)
		'''
        self.cursor.execute(query)
        self.conn.commit()

    def create_table_ingredients(self) -> None:
        """creates the ingredients table if it doesn't exist already"""
        table_sql = '''
		    CREATE TABLE IF NOT EXISTS ingredients (
				id INTEGER PRIMARY KEY AUTOINCREMENT,
                recipe_id INTEGER NOT NULL,
		        name TEXT NOT NULL,
		        quantity INTIGER,
		        unit TEXT,
                FOREIGN KEY (recipe_id)
				REFERENCES lists (id)
			)
		'''
        self.cursor.execute(table_sql)
        self.conn.commit()

    def create_table_shopping_list(self) -> None:
        """creates the shopping list table if it doesn't exist already"""
        table_sql = '''
		    CREATE TABLE IF NOT EXISTS shopping_list (
		        id INTEGER PRIMARY KEY AUTOINCREMENT,
		        name TEXT NOT NULL,
		        quantity INTIGER,
		        unit TEXT
			)
		'''
        self.cursor.execute(table_sql)
        self.conn.commit()

    def create_table_allergies(self) -> None:
        """creates the allergies table if it doesn't exist already"""

        table_sql = '''
		    CREATE TABLE IF NOT EXISTS allergies (
		        id INTEGER PRIMARY KEY AUTOINCREMENT,
				allergy TEXT NOT NULL
			)
		'''
        self.cursor.execute(table_sql)
        self.conn.commit()

    def create_table_dietary_restrictions(self) -> None:
        """creates the dietary_restrictions table if it doesn't exist already"""

        table_sql = '''
		    CREATE TABLE IF NOT EXISTS dietary_restrictions (
		        id INTEGER PRIMARY KEY AUTOINCREMENT,
				is_vegan BOOLEAN,
				is_vegetarian BOOLEAN,
				is_lactose_intolerant BOOLEAN
		    )
		'''
        self.cursor.execute(table_sql)
        self.conn.commit()

    def create_table_meal_plans(self) -> None:
        """Creates the meal_plans table if it doesn't exist already"""

        table_sql = '''
            CREATE TABLE IF NOT EXISTS meal_plans (
            date_saved TEXT,
            recipe_name TEXT
            )
        '''
        self.cursor.execute(table_sql)
        self.conn.commit()

    # testing
    def add_recipe(self, recipe: Recipe) -> None:
        """Adds a new recipe to the database"""
        recipe_tup = (
            recipe.name,
            recipe.calories,
            recipe.prep_time
        )
        ingredients = recipe.ingredients

        recipe_insert_cmd = '''
		    INSERT INTO recipes (
				name,
		        calories,
		        prep_time
			)
		    VALUES (?, ?, ?)
		'''

        self.cursor.execute(recipe_insert_cmd, recipe_tup)
        recipe_id = self.cursor.lastrowid

        for ingredient in ingredients:
            ingredient_tup = (
                recipe_id,
                ingredient.name,
                ingredient.quantity,
                ingredient.unit
            )

            ingredient_insert_cmd = '''
		    	INSERT INTO ingredients (
					recipe_id,
					name,
		        	quantity,
		        	unit
				)
		    	VALUES (?, ?, ?, ?)
			'''

            self.cursor.execute(ingredient_insert_cmd, ingredient_tup)

        self.conn.commit()

    def add_ingredient_to_shopping_list(self, new_ingredient: Ingredient) -> None:
        """Adds an ingredient to the shopping list.
        The quantity of the same ingredients with the same unit gets accumulated"""
        self.cursor.execute('SELECT * FROM shopping_list WHERE name = ?', (new_ingredient.name,))
        existing_ingredients = self.cursor.fetchall()
        is_added = False

        # Check if such ingredient is already added and  if units match
        if existing_ingredients is not None:
            for existing_ingredient in existing_ingredients:
                if new_ingredient.unit == existing_ingredient[3]:
                    updated_quantity = new_ingredient.quantity + existing_ingredient[2]

                    ingredient_tup = (
                        new_ingredient.name,
                        updated_quantity,
                        new_ingredient.unit,
                        existing_ingredient[0]
                    )

                    update_cmd = '''
                        UPDATE shopping_list
                        SET
                            name = ?,
                            quantity = ?,
                            unit = ?
                        WHERE id = (?)
                    '''
                    self.cursor.execute(update_cmd, ingredient_tup)
                    is_added = True

        if not is_added:
            new_ingredient_tup = (
                new_ingredient.name,
                new_ingredient.quantity,
                new_ingredient.unit
            )

            insert_cmd = '''
				INSERT INTO shopping_list (
					name,
					quantity,
					unit
				)
				VALUES (?, ?, ?)
			'''

            self.cursor.execute(insert_cmd, new_ingredient_tup)

        self.conn.commit()

    def add_user_info(self, user: User) -> None:
        """Add user info to he database"""
        self.cursor.execute('DELETE FROM allergies')
        self.cursor.execute('DELETE FROM dietary_restrictions')

        dietary_restrictions_tup = (
            user.is_vegan,
            user.is_vegetarian,
            user.is_lactose_intolerant
        )

        for allergy in user.allergies:
            self.cursor.execute('''INSERT INTO allergies (allergy) VALUES (?)''', (allergy,))

        insert_cmd = '''
				INSERT INTO dietary_restrictions (
					is_vegan,
					is_vegetarian,
					is_lactose_intolerant
				)
				VALUES (?, ?, ?)
			'''

        self.cursor.execute(insert_cmd, dietary_restrictions_tup)
        self.conn.commit()

    def add_planned_meal(self, date: str, name_of_recipe: str) -> None:
        """Adds a chosen meal and selected date to the database"""
        insert_pm = '''
            INSERT INTO meal_plans (
            date_saved, 
            recipe_name) 
            VALUES (?, ?)
        '''

        self.cursor.execute(insert_pm, (date, name_of_recipe))
        self.conn.commit()

    def delete_ingredient_from_shopping_list(self, ingredient: Ingredient) -> None:
        """Deletes the specified ingredient from the shopping list"""
        self.cursor.execute("DELETE FROM shopping_list WHERE name = ?", (ingredient.name,))
        self.conn.commit()

    # testing
    def retrieve_recipes(self) -> list[Recipe]:
        """Returns a list of all the recipes that are stored in the database"""
        self.cursor.execute('SELECT * FROM recipes')
        recipes = self.cursor.fetchall()
        recipes_list = []

        # Iterate through all the rows in recipe table and create recipe objects
        for recipe in recipes:
            recipe_id = recipe[0]
            ingredient_select_cmd = 'SELECT * FROM ingredients WHERE recipe_id = ?'
            self.cursor.execute(ingredient_select_cmd, (recipe_id,))
            ingredients = self.cursor.fetchall()
            ingredients_list = []

            for ingredient in ingredients:
                info = self.get_ingredient_info(ingredient[2])
                ingredient_obj = Ingredient(
                    ingredient[2],
                    quantity=ingredient[3],
                    unit=ingredient[4],
                    is_vegan=info['is_vegan'],
                    is_vegetarian=info['is_vegetarian'],
                    is_lactose_free=info['is_lactose_free']
                )

                ingredients_list.append(ingredient_obj)

            recipe_obj = Recipe(
                recipe[1],
                calories=recipe[2],
                prep_time=recipe[3],
                ingredients=ingredients_list
            )

            recipes_list.append(recipe_obj)

        return recipes_list

    def retrieve_shopping_list(self) -> list[Ingredient]:
        """Returns a list of all the ingredients that are stored in the shopping list"""
        self.cursor.execute('SELECT * FROM shopping_list')
        shopping_list_raw = self.cursor.fetchall()

        shopping_list = []

        for ingredient in shopping_list_raw:
            ingredient_obj = Ingredient(
                ingredient[1],
                quantity=ingredient[2],
                unit=ingredient[3]
            )

            shopping_list.append(ingredient_obj)

        return shopping_list

    def retrieve_user_info(self) -> User:
        """retrieve a user object that has all the attributes set from the database"""
        self.cursor.execute('SELECT allergy FROM allergies')
        allergies_raw = self.cursor.fetchall()
        allergies = set()
        for allergy in allergies_raw:
            allergies.add(allergy[0])
        self.cursor.execute('SELECT * FROM dietary_restrictions')
        dietary_restrictions = self.cursor.fetchall()
        is_vegan = dietary_restrictions[0][1]
        is_vegetarian = dietary_restrictions[0][2]
        is_lactose_intolerant = dietary_restrictions[0][3]

        user = User(
            allergies=allergies,
            is_vegan=is_vegan,
            is_vegetarian=is_vegetarian,
            is_lactose_intolerant=is_lactose_intolerant)
        return user

    def retrieve_planned_meal(self, selected_date: str) -> str:     # add type hint
        """Returns the chosen meal on the selected date"""
        self.cursor.execute('SELECT recipe_name '
                            'FROM meal_plans '
                            'WHERE date_saved=?', (selected_date,))
        planned_meals_raw = self.cursor.fetchall()   # this is a list, needs to be str

        planned_meal = ""
        if len(planned_meals_raw) != 0:
            planned_meal = planned_meals_raw[0][0]

        return planned_meal

    def csv_to_database(self, filename: str) -> None:
        """Converts a csv file to a database table"""
        df_path = os.path.join(self.project_folder, filename)
        df = pd.read_csv(df_path)
        df.to_sql('calories_and_categories', self.conn, index=False, if_exists='replace')
        self.conn.commit()

    def get_ingredient_info(self, ingredient: str) -> dict[str, bool]:
        """Returns a dictionary with information about the ingredient"""
        self.cursor.execute(
            'SELECT * FROM calories_and_categories WHERE FoodItem = ? COLLATE NOCASE', (ingredient,)
            )
        data = self.cursor.fetchone()
        info = {}
        if data:
            info['is_vegan'] = data[5]
            info['is_vegetarian'] = data[6]
            info['is_lactose_free'] = data[7]
        else:
            print(f'{ingredient} has no info. Please update (True/False)')
            info['is_vegan'] = bool(int(input('Is it vegan? ')))
            info['is_vegetarian'] = bool(int(input('Is it vegetarian? ')))
            info['is_lactose_free'] = bool(int(input('Is it lactose free? ')))
            self.add_new_ingredient_info(ingredient, info)
        return info

    def add_new_ingredient_info(self, ingredient_name, ingredient_info: dict[str, bool]) -> None:
        """Adds a new ingredient to the database"""
        ingredient_info_tup = (
            ingredient_name,
            ingredient_info['is_vegan'],
            ingredient_info['is_vegetarian'],
            ingredient_info['is_lactose_free'],
        )

        insert_cmd = '''
				INSERT INTO calories_and_categories (
					FoodItem,
					Vegan,
					Vegetarian,
					LactoseFree
				)
				VALUES (?, ?, ?, ?)
		'''

        self.cursor.execute(insert_cmd, ingredient_info_tup)
        self.conn.commit()
