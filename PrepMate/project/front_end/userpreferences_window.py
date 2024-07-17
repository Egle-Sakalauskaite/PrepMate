"""
This module contains the class for the User Preferences window.
"""
from typing import TYPE_CHECKING
from PySide6.QtWidgets import (QPushButton, QWidget, QVBoxLayout, QGroupBox, QHBoxLayout,
                               QBoxLayout, QLabel, QSpinBox, QComboBox, QCheckBox, QLineEdit)

if TYPE_CHECKING:
    from project.__main__ import PrepMateWindow


class UserPreferencesWindow(QWidget):
    """
    QWidget for setting the user's preferences for recipe suggestions.
    """

    def __init__(self, prepmate_window: "PrepMateWindow") -> None:
        super().__init__()
        self.list_lineedits_cantcontain: list[QLineEdit]
        self.list_lineedits_musthaves: list[QLineEdit]
        self.prepmate_window = prepmate_window

        button_back_to_main = QPushButton("Back to Main Menu")
        button_back_to_main.clicked.connect(prepmate_window.to_mainmenuwindow)
        button_to_suggestions = QPushButton("Go to Suggestions")
        # button_to_suggestions.clicked.connect(prepmate_window.to_suggestionswindow)
        button_to_suggestions.clicked.connect(
            lambda: self.save_input(self.list_lineedits_musthaves,
                                    self.list_lineedits_cantcontain))

        explanatory_text = QLabel(
            "In this window you can set your preferences for the suggested recipes.")

        # Cooking Duration
        box_cookingduration = QGroupBox("Cooking Duration")
        label_duration = QLabel("Choose maximum preparation time:")
        self.combobox_duration = QComboBox()
        self.combobox_duration.addItems(("None", "20 mins", "30 mins", "40 mins",
                                         "60 mins", "90 mins", "120 mins"))
        layout_duration = QHBoxLayout()
        layout_duration.addWidget(label_duration)
        layout_duration.addWidget(self.combobox_duration)
        box_cookingduration.setLayout(layout_duration)

        # Calorie Intake
        box_calorieintake = QGroupBox("Calorie Intake")
        label_calorie = QLabel("Enter a range for the caloric intake:")
        self.checkbox_calorieintake = QCheckBox("I don't want to filter based on calories.")
        self.checkbox_calorieintake.toggled.connect(self.toggled_checkbox)
        self.spinbox_mincal = QSpinBox()
        self.spinbox_mincal.setMaximum(9999)
        self.spinbox_maxcal = QSpinBox()
        self.spinbox_maxcal.setMaximum(9999)
        # Make sure the default of the window is: don't take the calories into account
        self.checkbox_calorieintake.setChecked(True)

        inner_layout_calories = QHBoxLayout()
        inner_layout_calories.addWidget(QLabel("Min:"))
        inner_layout_calories.addWidget(self.spinbox_mincal)
        inner_layout_calories.addWidget(QLabel("Max:"))
        inner_layout_calories.addWidget(self.spinbox_maxcal)
        outer_layout_calories = QVBoxLayout()
        outer_layout_calories.addWidget(label_calorie)
        outer_layout_calories.addLayout(inner_layout_calories)
        outer_layout_calories.addWidget(self.checkbox_calorieintake)
        box_calorieintake.setLayout(outer_layout_calories)

        # must-have ingredients
        box_musthave = self.create_must_have_groupbox()

        # Can't Contain ingredient
        box_cantcontain = self.create_cant_contain_groupbox()

        # Combining all the components:
        main_layout = QVBoxLayout()
        main_layout.addWidget(button_back_to_main)
        main_layout.addWidget(explanatory_text)
        main_layout.addWidget(box_cookingduration)
        main_layout.addWidget(box_calorieintake)
        main_layout.addWidget(box_musthave)
        main_layout.addWidget(box_cantcontain)
        main_layout.addWidget(button_to_suggestions)
        self.setLayout(main_layout)

    @staticmethod
    def add_line(layout: QBoxLayout, lines: list[QLineEdit]) -> None:
        """Method to add a QLineEdit to a layout and an accompanying list."""
        new_line = QLineEdit()
        layout.addWidget(new_line)
        lines.append(new_line)

    @staticmethod
    def delete_line(layout: QBoxLayout, lines: list[QLineEdit]) -> None:
        """Method to delete a QLineEdit from a layout and an accompanying list."""
        if len(lines) > 1:
            layout.removeWidget(lines[-1])
            lines[-1].deleteLater()
            lines.pop(-1)

    def toggled_checkbox(self) -> None:
        """Method that switches the QLineEdit's for the calories from
            editable to non-editable."""
        if self.spinbox_maxcal.isReadOnly():
            self.spinbox_maxcal.setReadOnly(False)
            self.spinbox_maxcal.setStyleSheet("color: black")
            self.spinbox_mincal.setReadOnly(False)
            self.spinbox_mincal.setStyleSheet("color: black")

        else:
            self.spinbox_maxcal.setReadOnly(True)
            self.spinbox_maxcal.setStyleSheet("color: white")
            self.spinbox_mincal.setReadOnly(True)
            self.spinbox_mincal.setStyleSheet("color: white")

    def save_input(self, list_must_have: list[QLineEdit],
                   list_cant_contain: list[QLineEdit]) -> None:
        """Method that retrieves the user's preference input, and passes
        it to the Suggestion Window."""
        preferences_given = False

        # Must haves
        must_have_names = []
        for lineedit in list_must_have:
            must_have_names.append(lineedit.text().strip().capitalize())
        if len(must_have_names) == 1 and must_have_names[0] == "":
            must_have_names.pop(0)
        if len(must_have_names) > 0:
            preferences_given = True

        # Should not haves
        cant_contain_names = []
        for lineedit in list_cant_contain:
            cant_contain_names.append(lineedit.text().strip().capitalize())
        if len(cant_contain_names) == 1 and cant_contain_names[0] == "":
            cant_contain_names.pop(0)
        if len(cant_contain_names) > 0:
            preferences_given = True

        # Calorie min max
        if self.checkbox_calorieintake.isChecked():
            calorie_min_max = None
        else:
            calorie_min_max = (self.spinbox_mincal.value(), self.spinbox_maxcal.value())
            preferences_given = True

        # Max time
        chosen_time_str = self.combobox_duration.currentText()
        if chosen_time_str == "None":
            chosen_time = None
        else:
            chosen_time_str = chosen_time_str[:-5]
            chosen_time = int(chosen_time_str)
            preferences_given = True

        if preferences_given:
            user_preference_info = (
                must_have_names,
                cant_contain_names,
                calorie_min_max,
                chosen_time
            )
        else:
            user_preference_info = None

        self.prepmate_window.to_suggestionswindow(user_preference_info)

    def create_must_have_groupbox(self) -> QGroupBox:
        """Method that creates a QGroupbox containing the interface
        for the Must-Have ingredients"""
        box_musthave = QGroupBox("Must-Have Ingredients")
        label_musthave = QLabel("If there are any ingredients that must "
                                "be used in a recipe,\nwrite them down here:")

        # Creating a list of QLineEdits (input fields):
        layout_lineedits_musthave = QVBoxLayout()
        lineedit_musthave_0 = QLineEdit()
        self.list_lineedits_musthaves = [lineedit_musthave_0]
        layout_lineedits_musthave.addWidget(lineedit_musthave_0)

        # Creating the buttons:
        button_addmusthave = QPushButton("Add Ingredient")
        button_addmusthave.clicked.connect(
            lambda: self.add_line(layout_lineedits_musthave,
                                  self.list_lineedits_musthaves))
        button_deletemusthave = QPushButton("Delete Ingredient")
        button_deletemusthave.clicked.connect(
            lambda: self.delete_line(layout_lineedits_musthave,
                                     self.list_lineedits_musthaves))
        layout_musthavebuttons = QHBoxLayout()
        layout_musthavebuttons.addWidget(button_addmusthave)
        layout_musthavebuttons.addWidget(button_deletemusthave)

        # Combining components in layout:
        layout_musthaves = QVBoxLayout()
        layout_musthaves.addWidget(label_musthave)
        layout_musthaves.addLayout(layout_musthavebuttons)
        layout_musthaves.addLayout(layout_lineedits_musthave)
        box_musthave.setLayout(layout_musthaves)
        return box_musthave

    def create_cant_contain_groupbox(self) -> QGroupBox:
        """Method that creates a QGroupbox containing the interface
                for the Can't-Contain ingredients"""
        box_cantcontain = QGroupBox("Can't-Contain Ingredients")
        label_cantcontain = QLabel("If you want to exclude recipes that "
                                   "contain certain ingredients,"
                                   "\n you can write them down here:")

        # Creating a list of QLineEdits (input fields):
        layout_lineedits_cantcontain = QVBoxLayout()
        lineedit_cantcontain_0 = QLineEdit()
        self.list_lineedits_cantcontain = [lineedit_cantcontain_0]
        layout_lineedits_cantcontain.addWidget(lineedit_cantcontain_0)

        # Creating the buttons:
        button_addcantcontain = QPushButton("Add Ingredient")
        button_addcantcontain.clicked.connect(
            lambda: self.add_line(layout_lineedits_cantcontain,
                                  self.list_lineedits_cantcontain))
        button_deletecantcontain = QPushButton("Delete Ingredient")
        button_deletecantcontain.clicked.connect(
            lambda: self.delete_line(layout_lineedits_cantcontain,
                                     self.list_lineedits_cantcontain))
        layout_cantcontainbuttons = QHBoxLayout()
        layout_cantcontainbuttons.addWidget(button_addcantcontain)
        layout_cantcontainbuttons.addWidget(button_deletecantcontain)

        # Combining components in layout:
        layout_cantcontain = QVBoxLayout()
        layout_cantcontain.addWidget(label_cantcontain)
        layout_cantcontain.addLayout(layout_cantcontainbuttons)
        layout_cantcontain.addLayout(layout_lineedits_cantcontain)
        box_cantcontain.setLayout(layout_cantcontain)
        return box_cantcontain
