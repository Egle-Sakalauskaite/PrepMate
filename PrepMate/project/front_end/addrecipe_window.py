"""This  module contains the classes for the add user recipe window."""


from PySide6.QtWidgets import (QWidget, QPushButton, QVBoxLayout, QLineEdit, QLabel, QComboBox,
                               QSpinBox, QGridLayout, QHBoxLayout, QCheckBox, QScrollArea, QDialog)
from PySide6.QtCore import Qt
from project.back_end.save_user_recipe import save_user_recipe


class AddRecipeWindow(QWidget):
    """This class represents the add user recipe window."""
    def __init__(self, prepmate_window) -> None:
        super().__init__()
        self.prepmate_window = prepmate_window
        layout = QVBoxLayout()

        # Back to Main Menu button
        button_back_to_main = QPushButton("Back to Main Menu")
        button_back_to_main.clicked.connect(self.prepmate_window.to_mainmenuwindow)
        layout.addWidget(button_back_to_main)

        # Explanation
        explanation = QLabel("In this window you can add your own recipes to the database by"
                             "\nfilling in the required information and clicking te save button.")
        layout.addWidget(explanation)

        # Recipe Title
        recipe_title_label = QLabel("Recipe Title")
        recipe_title_label.setStyleSheet("QLabel {color: black; font-weight: bold;}")
        self.recipe_title = QLineEdit()
        layout.addWidget(recipe_title_label)
        layout.addWidget(self.recipe_title)

        # Prep Time
        prep_time_label = QLabel("Prep Time (minutes)")
        prep_time_label.setStyleSheet("QLabel {color: black; font-weight: bold;}")
        self.prep_time = QSpinBox()
        self.prep_time.setMaximum(99999)
        layout.addWidget(prep_time_label)
        layout.addWidget(self.prep_time)

        # Calories
        calorie_label = QLabel("Calories (kcal)")
        calorie_label.setStyleSheet("QLabel {color: black; font-weight: bold;}")
        self.calories = QSpinBox()
        self.calories.setMaximum(99999)
        layout.addWidget(calorie_label)
        layout.addWidget(self.calories)

        # Ingredients
        ingredients_label = QLabel("Ingredients")
        ingredients_label.setStyleSheet("QLabel {color: black; font-weight: bold;}")
        self.ingredient_list = IngredientList()
        layout.addWidget(ingredients_label)
        layout.addWidget(self.ingredient_list)

        # Instructions
        instructions_label = QLabel("Instructions")
        instructions_label.setStyleSheet("QLabel {color: black; font-weight: bold;}")
        self.instruction_list = InstructionList()
        layout.addWidget(instructions_label)
        layout.addWidget(self.instruction_list)

        # Save Recipe button
        save_button = QPushButton("Save Recipe")
        save_button.clicked.connect(lambda: self.save(self))
        layout.addWidget(save_button)

        # Set the layout
        widget = QWidget()
        widget.setLayout(layout)
        self.addrecipe_scroll: QScrollArea = QScrollArea()
        self.addrecipe_scroll.setVerticalScrollBarPolicy(Qt.ScrollBarPolicy.ScrollBarAlwaysOn)
        self.addrecipe_scroll.setHorizontalScrollBarPolicy(Qt.ScrollBarPolicy.ScrollBarAlwaysOff)
        self.addrecipe_scroll.setWidgetResizable(True)
        self.addrecipe_scroll.setWidget(widget)

    @staticmethod
    def save(recipe) -> None:
        """Collecting the information from the QLineEdits and
        adding the info to the database using the back end"""
        ingredients = [
            [ingredient.name.text(), int(ingredient.quantity.value()),
             ingredient.unit.currentText(), bool(ingredient.vegan.clicked),
             bool(ingredient.vegetarian.clicked), bool(ingredient.lactose_free.clicked)]
            for ingredient in recipe.ingredient_list.ingredient_lines
        ]
        instructions = [line.text() for line in recipe.instruction_list.instruction_lines]
        add_recipe = save_user_recipe((
            recipe.recipe_title.text(),
            int('0'+recipe.calories.text()),
            int('0'+recipe.prep_time.text()),
            ingredients,
            instructions
        ))

        recipe.create_popup(add_recipe)

    def create_popup(self, error: int) -> None:
        """Create a popup that confirms the
        recipe has been added to the database"""
        popup = QDialog(self)
        popup.setWindowTitle("PrepMate - Error Adding Recipe")

        if error is None:
            popup.setWindowTitle("PrepMate - Recipe Added")
            label = QLabel("The recipe has successfully been added to the database!")
        elif error == 0:
            label = QLabel("Please enter a title for the recipe.")
            label.setStyleSheet("QLabel {color: red; font-weight: bold;}")
        elif error == 1:
            label = QLabel("This recipe already exists.\nPlease choose another title.")
            label.setStyleSheet("QLabel {color: red; font-weight: bold;}")
        elif error == 2:
            label = QLabel("Please add at least one ingredient to the recipe.")
            label.setStyleSheet("QLabel {color: red; font-weight: bold;}")
        elif error == 3:
            label = QLabel("The recipe title is invalid. Only letters,"
                           "\nnumbers, whitespaces, '-', and ',' are allowed.")
            label.setStyleSheet("QLabel {color: red; font-weight: bold;}")
        elif error == 4:
            label = QLabel("Please make sure each\ningredient has a unit.")
            label.setStyleSheet("QLabel {color: red; font-weight: bold;}")
        else:
            label = QLabel("There was an error adding the recipe to the database.")
            label.setStyleSheet("QLabel {color: red; font-weight: bold;}")

        label.setAlignment(Qt.AlignmentFlag.AlignCenter)

        ok_button = QPushButton("OK")
        ok_button.clicked.connect(popup.close)

        layout = QVBoxLayout()
        layout.addWidget(label)
        layout.addWidget(ok_button)
        popup.setLayout(layout)
        popup.exec_()

        # Back to the main menu if the recipe was added
        if error is None:
            self.prepmate_window.to_mainmenuwindow()


class IngredientList(QWidget):
    """This class represents the ingredient list"""
    def __init__(self) -> None:
        super().__init__()
        self.list_layout: QGridLayout = QGridLayout()
        self.ingredient_lines: list[IngredientLine] = []

        add_button = QPushButton("Add Ingredient")
        add_button.clicked.connect(self.add_line)
        self.list_layout.addWidget(add_button, 0, 0)

        del_button = QPushButton("Delete Ingredient")
        del_button.clicked.connect(self.del_line)
        self.list_layout.addWidget(del_button, 0, 1)

        self.instruction_label = QLabel("Fill in the ingredients "
                                        "needed for 1 serving of the recipe."
                                        "\nUse the checkboxes to indicate that the ingredient is"
                                        "\nvegan, vegetarian or lactose free respectively.")
        self.list_layout.addWidget(self.instruction_label, 1, 0, 1, 2)

        self.setLayout(self.list_layout)

    def add_line(self) -> None:
        """Adds a line to the ingredient list"""
        line = IngredientLine()
        self.ingredient_lines.append(line)
        self.list_layout.addWidget(line, len(self.ingredient_lines)+2, 0, 1, 2)

    def del_line(self) -> None:
        """Removes a line from the ingredient list"""
        if len(self.ingredient_lines) > 1:
            self.list_layout.removeWidget(self.ingredient_lines[-1])
            self.ingredient_lines[-1].deleteLater()
            self.ingredient_lines.pop(-1)


class IngredientLine(QWidget):
    """This class represents one line of the ingredient list"""
    def __init__(self) -> None:
        super().__init__()
        layout = QHBoxLayout()
        self.name = QLineEdit()
        self.name.setPlaceholderText("Name")

        self.quantity = QSpinBox()
        self.quantity.setMaximum(99999)

        self.unit = QComboBox()
        self.unit.setPlaceholderText("Unit")
        self.unit.addItem("g")
        self.unit.addItem("ml")
        self.unit.addItem("piece")

        self.vegan = QCheckBox()
        self.vegetarian = QCheckBox()
        self.lactose_free = QCheckBox()

        layout.addWidget(self.name)
        layout.addWidget(self.quantity)
        layout.addWidget(self.unit)
        layout.addWidget(self.vegan)
        layout.addWidget(self.vegetarian)
        layout.addWidget(self.lactose_free)

        self.setLayout(layout)


class InstructionList(QWidget):
    """This class represents the instruction list"""
    def __init__(self) -> None:
        super().__init__()
        self.list_layout = QGridLayout()
        self.instruction_lines: list[QLineEdit] = []

        add_button = QPushButton("Add Instruction Step")
        add_button.clicked.connect(self.add_line)
        self.list_layout.addWidget(add_button, 0, 0)

        del_button = QPushButton("Delete Instruction Step")
        del_button.clicked.connect(self.del_line)
        self.list_layout.addWidget(del_button, 0, 1)

        self.instruction_label = QLabel("Write each instruction step on a separate line.")
        self.list_layout.addWidget(self.instruction_label, 1, 0, 1, 2)

        self.setLayout(self.list_layout)

    def add_line(self) -> None:
        """This method adds a line to the instruction list"""
        line = QLineEdit()
        line.setPlaceholderText(f"Step {len(self.instruction_lines)+1}")
        self.instruction_lines.append(line)
        self.list_layout.addWidget(line, len(self.instruction_lines)+1, 0, 1, 2)

    def del_line(self) -> None:
        """This method deletes a line from the instruction list"""
        if len(self.instruction_lines) > 0:
            self.list_layout.removeWidget(self.instruction_lines[-1])
            self.instruction_lines[-1].deleteLater()
            self.instruction_lines.pop(-1)
