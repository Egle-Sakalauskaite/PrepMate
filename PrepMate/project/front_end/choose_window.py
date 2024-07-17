"""This module contains the code for the 'choose window':
the window that pops up when the user clicks on the 'choose button'
in the suggestions window"""


from PySide6.QtWidgets import (QWidget, QLabel, QGridLayout, QPushButton,
                               QGroupBox, QScrollArea, QComboBox, QDialog, QVBoxLayout)
from PySide6.QtCore import Qt, QDate
from project.back_end.recipe import Recipe
from project.back_end.database import Database
from project.back_end.ingredient import Ingredient
from project.back_end.scale_ingredients import scale_ingredients


class IngredientBox(QWidget):
    """This class represents the box in the choose window
    where the ingredients for the recipe are listed"""
    def __init__(self, ingredient_list: list) -> None:
        """Create a GroupBox that shows
        the ingredients in the recipe."""
        super().__init__()
        self.ingredient_list = ingredient_list

        # Create a GridLayout
        self.box_layout = QGridLayout()

        # Create labels for the ingredients and add them to the GridLayout
        v_index = 0
        for ingredient in self.ingredient_list:
            ingredient_name = QLabel(ingredient.name)
            ingredient_quantity = QLabel(str(ingredient.quantity))
            ingredient_unit = QLabel(ingredient.unit)
            self.box_layout.addWidget(ingredient_name, v_index, 0, 1, 2)
            self.box_layout.addWidget(ingredient_quantity, v_index, 2, 1, 1)
            self.box_layout.addWidget(ingredient_unit, v_index, 3, 1, 1)
            v_index += 1

        # Create the GroupBox and ScrollArea
        self.box = QGroupBox("Ingredients")
        self.box.setLayout(self.box_layout)
        self.box_scroll = QScrollArea()
        self.box_scroll.setWidget(self.box)
        self.box_scroll.setWidgetResizable(True)
        # self.box_scroll.setFixedSize(380, 400)


class InstructionsBox(QWidget):
    """This class represents the box in the choose window
        where the ingredients for the recipe are listed"""

    def __init__(self, instructions_list: list[str]) -> None:
        """Create a GroupBox that shows
        the instructions of the recipe."""
        super().__init__()
        self.instructions_list = instructions_list

        # Create a box layout:
        self.instructions_layout = QVBoxLayout()

        # Create labels for the ingredients and add them to the GridLayout
        for i, instruction in enumerate(self.instructions_list):
            instruction_label = QLabel(f'{i+1}: {instruction}')
            instruction_label.setWordWrap(True)
            self.instructions_layout.addWidget(instruction_label)

        # Create the GroupBox and ScrollArea
        self.instructions_box = QGroupBox("Instructions")
        self.instructions_box.setLayout(self.instructions_layout)
        self.instructions_scroll = QScrollArea()
        self.instructions_scroll.setWidget(self.instructions_box)
        self.instructions_scroll.setWidgetResizable(True)


class ChooseWindow(QWidget):
    """This class represents the choose window"""
    def __init__(self, recipe: Recipe) -> None:
        """Create a choose window for the recipe"""
        super().__init__()
        self.recipe = recipe
        self.db = Database('PrepMate.db')
        self.scaled_ingredients: None | list[Ingredient] = None

        # Create a window
        self.setWindowTitle(f"PrepMate - {self.recipe.name}")
        self.setGeometry(610, 100, 600, 600)

        # Create a GridLayout
        self.choose_layout = QGridLayout()

        # Create labels for the name, calories and prep time and add them to the layout
        name = QLabel(self.recipe.name)
        name.setAlignment(Qt.AlignmentFlag.AlignCenter)     # Don't use Qt.AlignCenter
        name.setStyleSheet("QLabel {color: black; font-weight: bold;}")
        prep_time = QLabel("Preparation time:         " + str(self.recipe.prep_time) + " mins")
        prep_time.setAlignment(Qt.AlignmentFlag.AlignCenter)
        cals = QLabel(f"Calories per serving:  {self.recipe.calories}")
        cals.setAlignment(Qt.AlignmentFlag.AlignCenter)
        self.choose_layout.addWidget(name, 0, 1, 1, 2)
        self.choose_layout.addWidget(cals, 1, 1, 1, 2)
        self.choose_layout.addWidget(prep_time, 2, 1, 1, 2)

        # Add the recipe properties to the layout
        h_index = 1
        if self.recipe.is_vegan:
            vegan_label = QLabel("Vegan")
            vegan_label.setStyleSheet("QLabel {color: green; font-weight: bold;}")
            self.choose_layout.addWidget(vegan_label, 3, h_index, 1, 1)
            h_index += 1
        elif self.recipe.is_vegetarian:
            vegetarian_label = QLabel("Vegetarian")
            vegetarian_label.setStyleSheet("QLabel {color: darkGreen; font-weight: bold;}")
            self.choose_layout.addWidget(vegetarian_label, 3, h_index, 1, 1)
            h_index += 1
        if self.recipe.is_lactose_free:
            lactose_free_label = QLabel("Lactose free")
            lactose_free_label.setStyleSheet("QLabel {color: blue; font-weight: bold;}")
            self.choose_layout.addWidget(lactose_free_label, 3, h_index, 1, 1)
            h_index += 1

        # Create the GroupBox for the ingredient list and add it to the layout
        ingredients_box = IngredientBox(self.recipe.ingredients)
        instructions_box = InstructionsBox(self.recipe.instructions)
        self.choose_layout.addWidget(ingredients_box.box_scroll, 4, 0, 1, 2)
        self.choose_layout.addWidget(instructions_box.instructions_scroll, 4, 2, 1, 2)

        # Create a ComboBox to set the amount of servings
        self.servings = QComboBox(self)

        self.meal_plans = QComboBox(self)
        self.current_date = QDate.currentDate()
        self.create_combobox()

        # Add a cancel button and confirm button to the bottom of the layout
        cancel_button = QPushButton("Cancel")
        cancel_button.clicked.connect(self.close)
        choose_button = QPushButton("Choose")
        choose_button.clicked.connect(self.choose_action)
        self.choose_layout.addWidget(cancel_button, 6, 0, 1, 2)
        self.choose_layout.addWidget(choose_button, 6, 2, 1, 2)

        self.setLayout(self.choose_layout)

    def create_combobox(self) -> None:
        """Creates a ComboBow to select a day for the chosen meal and adds it to the layout"""
        servings_label = QLabel("Amount of servings:")
        servings_label.setAlignment(Qt.AlignmentFlag.AlignRight)  # Don't use Qt.AlignRight
        servings_options = ("1", "2", "3", "4", "5", "6", "7", "8", "9", "10", "11", "12")
        self.servings.addItems(servings_options)
        self.servings.setCurrentIndex(servings_options.index("1"))
        self.choose_layout.addWidget(servings_label, 5, 0, 1, 1)  # 8 0 1 2
        self.choose_layout.addWidget(self.servings, 5, 1, 1, 1)  # 8 2 1 1

        meal_plan_label = QLabel("Selected day:")
        meal_plan_label.setAlignment(Qt.AlignmentFlag.AlignRight)
        date_options: tuple[str, ...] = ("",)
        weekdays = {1: "Mon", 2: "Tue", 3: "Wed", 4: "Thu", 5: "Fri", 6: "Sat", 7: "Sun"}
        for i in range(8):
            date = self.current_date.addDays(i)
            day_int = date.dayOfWeek()
            day = weekdays[day_int]
            date_str = f'{date.day()}-{date.month()}'
            date_options = date_options + tuple((f"{day} ({date_str})",))

        self.meal_plans.addItems(date_options)
        self.meal_plans.setCurrentIndex(date_options.index(""))
        self.choose_layout.addWidget(meal_plan_label, 5, 2, 1, 1)
        self.choose_layout.addWidget(self.meal_plans, 5, 3, 1, 1)

    def choose_action(self) -> None:
        """This code is executed when the choose button
        is clicked in the choose window"""

        # Scale the ingredients to the amount of servings
        servings_int = int(self.servings.currentText())
        self.scaled_ingredients = scale_ingredients(self.recipe.ingredients, servings_int)

        # Add the scaled ingredients to the shoppinglist
        for ingredient in self.scaled_ingredients:
            self.db.add_ingredient_to_shopping_list(ingredient)

        # Save chosen meal and selected day in the database
        label_4 = QLabel("")
        self.db.create_table_meal_plans()
        if self.meal_plans.currentText() != "":
            date_to_db = self.meal_plans.currentText()[5:-1] + f"-{self.current_date.year()}"
            self.db.add_planned_meal(date_to_db, self.recipe.name)
            label_4 = QLabel(f"This meal has been planned on {date_to_db} in your calendar!")

        # Create a popup that confirms the ingredients have been added to the shoppinglist
        confirmation = QDialog(self)
        confirmation.setWindowTitle("PrepMate - Items added")
        label_1 = QLabel(f"The ingredients for {servings_int} servings of")
        label_2 = QLabel(f"'{self.recipe.name}'")
        label_3 = QLabel("have been added to your shoppinglist!")
        label_1.setAlignment(Qt.AlignmentFlag.AlignCenter)      # Don't use Qt.AlignCenter
        label_2.setAlignment(Qt.AlignmentFlag.AlignCenter)      # Don't use Qt.AlignCenter
        label_3.setAlignment(Qt.AlignmentFlag.AlignCenter)      # Don't use Qt.AlignCenter

        ok_button = QPushButton("OK")
        ok_button.clicked.connect(confirmation.close)

        layout = QVBoxLayout()
        layout.addWidget(label_1)
        layout.addWidget(label_2)
        layout.addWidget(label_3)
        if bool(label_4):
            layout.addWidget(label_4)
        layout.addWidget(ok_button)
        confirmation.setLayout(layout)
        confirmation.exec_()

        # Close the choose window
        self.close()
