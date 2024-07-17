"""This  module contains the class for the suggestions window."""


from typing import TYPE_CHECKING
from PySide6.QtWidgets import (QWidget, QGridLayout, QLabel, QVBoxLayout, QHBoxLayout,
                               QPushButton, QScrollArea, QGroupBox)
from PySide6.QtCore import Qt
from project.front_end.choose_window import ChooseWindow
from project.back_end.recipe_suggestions import Suggestions
from project.back_end.recipe import Recipe
if TYPE_CHECKING:
    from project.__main__ import PrepMateWindow


class RecipeWidget(QWidget):
    """This class creates the widget for the given recipe"""
    def __init__(self, recipe: Recipe) -> None:
        """Create a GroupBox for 'recipe'."""
        super().__init__()
        self.recipe = recipe
        self.choose_window: None | ChooseWindow = None

        # Create labels for the name, calories and prep time
        name = QLabel(self.recipe.name)
        name.setAlignment(Qt.AlignmentFlag.AlignCenter)     # Don't use Qt.AlignCenter
        name.setStyleSheet("QLabel {color: black; font-weight: bold;}")
        calories = QLabel("Calories per serving:    " + str(self.recipe.calories))
        prep_time = QLabel("Preparation time:         " + str(self.recipe.prep_time) + " mins")

        # Create the 'choose button'
        choose_button = QPushButton("Choose")
        choose_button.clicked.connect(lambda: self.choose_action(self))

        # Create a GridLayout and add the labels and the button to it
        grid_layout = QGridLayout()
        grid_layout.addWidget(name, 0, 0, 1, 4)
        grid_layout.addWidget(calories, 1, 1)
        grid_layout.addWidget(prep_time, 2, 1)
        grid_layout.addWidget(choose_button, 3, 1, 1, 2)

        # Create a GroupBox
        self.box = QGroupBox()
        self.box.setLayout(grid_layout)
        self.box.setFixedSize(360, 120)

    @staticmethod
    def choose_action(recipe_object: "RecipeWidget") -> None:
        """Open the choose window for the recipe but
        only if it is not opened yet."""
        if recipe_object.choose_window is None:
            recipe_object.choose_window = ChooseWindow(recipe_object.recipe)
        recipe_object.choose_window.show()


class SuggestionsWindow(Suggestions, QWidget):
    """This clas is used to display the suggestions window."""
    def __init__(self, prepmate_window: "PrepMateWindow", user_preference_info) -> None:
        """Create a window with all the
        suggestions listed under each other."""
        Suggestions.__init__(self)
        QWidget.__init__(self)
        self.prepmate_window = prepmate_window

        # Use the back end to create random recipe suggestions
        if user_preference_info is not None:
            self.check_user_preferences(*user_preference_info)
        self.random_suggestions()

        # Create a 'back' button and a refresh button
        button_back_to_main = QPushButton("Back to Main Menu")
        button_back_to_main.clicked.connect(self.prepmate_window.to_mainmenuwindow)
        button_back_to_preferences = QPushButton("Back to Preferences")
        button_back_to_preferences.clicked.connect(self.prepmate_window.to_userpreferenceswindow)
        refresh_button = QPushButton("Refresh")
        refresh_button.clicked.connect(
            lambda: prepmate_window.to_suggestionswindow(user_preference_info))

        # Create an HBoxLayout for two buttons next to each other
        self.hbox = QHBoxLayout()
        self.hbox.addWidget(button_back_to_preferences)
        self.hbox.addWidget(refresh_button)

        # Create a VBoxLayout and add the buttons to it
        self.vbox = QVBoxLayout()
        self.vbox.addWidget(button_back_to_main)
        self.vbox.addLayout(self.hbox)

        # Create a widget for each recommended recipe and add it to the layout
        self.widget = QWidget()
        for recipe in self.suggestions:
            suggestion = RecipeWidget(recipe)
            self.vbox.addWidget(suggestion.box)
        self.widget.setLayout(self.vbox)

        # Create a ScrollArea and add the recipe widgets to it
        self.suggestion_scroll = QScrollArea()
        self.suggestion_scroll.setVerticalScrollBarPolicy(Qt.ScrollBarAlwaysOn)     # type: ignore
        self.suggestion_scroll.setHorizontalScrollBarPolicy(Qt.ScrollBarAlwaysOff)  # type: ignore
        self.suggestion_scroll.setWidgetResizable(True)
        self.suggestion_scroll.setWidget(self.widget)
