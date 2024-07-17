"""This module sets up the widget for the main menu window."""


from typing import TYPE_CHECKING
import os
from PySide6.QtWidgets import QWidget, QPushButton, QVBoxLayout, QLabel
from PySide6.QtCore import Qt, QSize
from PySide6.QtGui import QPixmap
if TYPE_CHECKING:
    from project.__main__ import PrepMateWindow


class MainMenuWindow(QWidget):
    """This class generates a window for the main menu."""
    def __init__(self, prepmate_window: "PrepMateWindow") -> None:
        super().__init__()
        self.prepmate_window = prepmate_window

        project_folder = os.path.dirname(__file__)
        file_path = os.path.abspath(os.path.join(project_folder[:-17], 'images', 'prepmate_logo2'))
        pixmap = QPixmap(file_path)

        self.logo = QLabel(self)
        self.logo.setPixmap(pixmap)
        self.logo.setScaledContents(True)
        pic_size = QSize(self.logo.width(), self.logo.height())
        self.logo.resize(pic_size)
        self.logo.setFixedSize(380, 200)

        self.button_info = QPushButton("User Information")
        self.button_recipes = QPushButton("Recipe Recommendations")
        self.button_shop_list = QPushButton("Shopping List")
        self.button_calendar = QPushButton("Meal Plan Calendar")
        self.button_add_recipe = QPushButton("Add Recipe")

        self.button_info.clicked.connect(self.button_userinfo_clicked)
        self.button_recipes.clicked.connect(self.button_suggestions_clicked)
        self.button_shop_list.clicked.connect(self.button_shoppinglist_clicked)
        self.button_calendar.clicked.connect(self.button_calendar_clicked)
        self.button_add_recipe.clicked.connect(self.button_add_recipe_clicked)

        layout = QVBoxLayout(self)
        layout.addWidget(self.logo, alignment=Qt.AlignmentFlag.AlignCenter)
        layout.addWidget(self.button_info)
        layout.addWidget(self.button_recipes)
        layout.addWidget(self.button_shop_list)
        layout.addWidget(self.button_calendar)
        layout.addWidget(self.button_add_recipe)

    def button_userinfo_clicked(self) -> None:
        """This method redirects the user to the user information window."""
        self.prepmate_window.to_userinformationwindow()

    def button_suggestions_clicked(self) -> None:
        """This method redirects the user to the user preferences_window, in
        preperation for the recipe suggestions window."""
        self.prepmate_window.to_userpreferenceswindow()

    def button_shoppinglist_clicked(self) -> None:
        """This method redirects the user to the shopping list window."""
        self.prepmate_window.to_shoppinglistwindow()

    def button_calendar_clicked(self) -> None:
        """This method redirects the user to the meal planning calendar window."""
        self.prepmate_window.to_calendarwindow()

    def button_add_recipe_clicked(self) -> None:
        """This method redirects the user to the add recipe window."""
        self.prepmate_window.to_addrecipewindow()
