"""Main method for starting the application."""

import sys

from PySide6.QtWidgets import QApplication, QMainWindow
from project.front_end.mainmenu_window import MainMenuWindow
from project.front_end.userinformation_window import UserInformationWindow
from project.front_end.shoppinglist_window import ShoppingListWindow
from project.front_end.suggestions_window import SuggestionsWindow
from project.front_end.userpreferences_window import UserPreferencesWindow
from project.front_end.mealplanning_window import MealPlanningWindow
from project.front_end.addrecipe_window import AddRecipeWindow
from project.back_end.user import User
from project.back_end.database import Database


class PrepMateWindow(QMainWindow):
    """
    The main QMainWindow of the application, which will contain
    other windows(widget) as centralWidget.
    """
    def __init__(self, app: QApplication) -> None:
        super().__init__()
        self.app = app
        self.setWindowTitle("PrepMate")
        self.setCentralWidget(MainMenuWindow(self))
        self.setGeometry(200, 100, 400, 600)

        self.database = Database("PrepMate.db")
        try:
            self.database.retrieve_user_info()
        except IndexError:
            self.database.add_user_info(User())

    def to_userinformationwindow(self) -> None:
        """
        Method to create an userinfo widget, and set it as the central widget,
        thus displaying it on the PrepMate Window.
        """
        self.setCentralWidget(UserInformationWindow(self))

    def to_shoppinglistwindow(self) -> None:
        """
        Method to create a shoppinglist widget, and set it as the central widget,
        thus displaying it on the PrepMate Window.
        """
        self.setCentralWidget(ShoppingListWindow(self).shopping_scroll)

    def to_mainmenuwindow(self) -> None:
        """
        Method to create a mainmenu widget, and set it as the central widget,
        thus displaying it on the PrepMate Window.
        """
        self.setCentralWidget(MainMenuWindow(self))

    def to_suggestionswindow(self, user_preference_info) -> None:
        """
        Method to create a recipe suggestions widget, and set it as the central widget,
        thus displaying it on the PrepMate Window.
        """
        self.setCentralWidget(SuggestionsWindow(self, user_preference_info).suggestion_scroll)

    def to_userpreferenceswindow(self) -> None:
        """
        Method to create a user preferences widget, and set it as the central widget,
        thus displaying it on the PrepMate Window.
        """
        self.setCentralWidget(UserPreferencesWindow(self))

    def to_calendarwindow(self) -> None:
        """
        Method to create a meal planning widget, and set it as the central widget,
        thus displaying it on the PrepMate Window.
        """
        self.setCentralWidget(MealPlanningWindow(self))

    def to_addrecipewindow(self) -> None:
        """
        Method to create a add recipe widget, and set it as the central widget,
        thus displaying it on the PrepMate Window.
        """
        self.setCentralWidget(AddRecipeWindow(self).addrecipe_scroll)



if __name__ == "__main__":
    application = QApplication(sys.argv)
    myApp = PrepMateWindow(application)
    myApp.show()
    application.exec()
