"""This module sets up the widget for the user information window."""


from typing import TYPE_CHECKING
from PySide6.QtWidgets import (QWidget, QVBoxLayout, QGroupBox, QCheckBox,
                               QLabel, QPushButton, QMessageBox)
from PySide6.QtCore import Qt
from project.back_end.user import User
if TYPE_CHECKING:
    from project.__main__ import PrepMateWindow


class UserInformationWindow(QWidget):
    """This class generates a window for the user information input."""
    def __init__(self, prepmate_window: "PrepMateWindow") -> None:
        super().__init__()
        self.prepmate_window = prepmate_window
        self.previous_userinfo = prepmate_window.database.retrieve_user_info()
        self.fa_set: set = set()
        self.dr_dict: dict = {'Lactose-free': False, 'Vegetarian': False, 'Vegan': False}

        # food allergies checkboxes
        self.allergy_checkboxes = {
            'eggs': QCheckBox('Eggs'),
            'milk': QCheckBox('Milk'),
            'gluten': QCheckBox('Gluten'),
            'peanuts': QCheckBox('Peanuts'),
            'fish': QCheckBox('Fish'),
            'soybeans': QCheckBox('Soybeans')
        }

        # dietary restrictions checkboxes
        self.dietary_checkboxes = {
            'lactose': QCheckBox('Lactose-free'),
            'vegetarian': QCheckBox('Vegetarian'),
            'vegan': QCheckBox('Vegan')
        }

        self.set_layout()

    def set_layout(self) -> None:
        """Method that sets the layout of the user information widget."""
        # Group box food allergies
        fa = QGroupBox('Food Allergies')
        for allergy, checkbox in self.allergy_checkboxes.items():
            toggle_method = getattr(self, f"{allergy}_box_toggled", None)

            if toggle_method and callable(toggle_method):
                checkbox.toggled.connect(toggle_method)

        # add checkboxes to layout dynamically
        fa_layout = QVBoxLayout()
        for checkbox in self.allergy_checkboxes.values():
            fa_layout.addWidget(checkbox)

        fa.setLayout(fa_layout)

        # group box dietary restrictions
        dr = QGroupBox('Dietary Restrictions')
        for restriction, checkbox in self.dietary_checkboxes.items():
            toggle_method = getattr(self, f"{restriction}_box_toggled", None)

            if toggle_method and callable(toggle_method):
                checkbox.toggled.connect(toggle_method)

        # add checkboxes to layout dynamically
        dr_layout = QVBoxLayout()
        for checkbox in self.dietary_checkboxes.values():
            dr_layout.addWidget(checkbox)

        dr.setLayout(dr_layout)

        # layout user info window
        layout = QVBoxLayout()
        self.retrieve_selected_options()        # andere locatie miss?
        title_text = QLabel("User Information")

        # buttons
        button_save = QPushButton("Save")
        button_save.clicked.connect(self.button_save_clicked)  # add pop up for save confirmation
        button_back_to_main = QPushButton("Back to Main Menu")
        button_back_to_main.clicked.connect(self.prepmate_window.to_mainmenuwindow)

        layout.addWidget(button_back_to_main)
        layout.addWidget(title_text, alignment=Qt.AlignCenter)  # type: ignore[attr-defined]
        layout.addWidget(fa)
        layout.addWidget(dr)
        layout.addWidget(button_save)

        self.setLayout(layout)

    def retrieve_selected_options(self) -> None:
        """Method retrieves previously selected food allergies and diet restrictions
         from database"""
        if self.previous_userinfo.is_vegan == 1:
            self.dietary_checkboxes['vegan'].setChecked(True)
        if self.previous_userinfo.is_vegetarian == 1:
            self.dietary_checkboxes['vegetarian'].setChecked(True)
        if self.previous_userinfo.is_lactose_intolerant == 1:
            self.dietary_checkboxes['lactose'].setChecked(True)
        if len(self.previous_userinfo.allergies) != 0:
            if 'Eggs' in self.previous_userinfo.allergies:
                self.allergy_checkboxes['eggs'].setChecked(True)
            if 'Milk' in self.previous_userinfo.allergies:
                self.allergy_checkboxes['milk'].setChecked(True)
            if 'Gluten' in self.previous_userinfo.allergies:
                self.allergy_checkboxes['gluten'].setChecked(True)
            if 'Peanuts' in self.previous_userinfo.allergies:
                self.allergy_checkboxes['peanuts'].setChecked(True)
            if 'Fish' in self.previous_userinfo.allergies:
                self.allergy_checkboxes['fish'].setChecked(True)
            if 'Soybeans' in self.previous_userinfo.allergies:
                self.allergy_checkboxes['soybeans'].setChecked(True)

    def button_save_clicked(self) -> None:
        """This method saves the user input and saves it in the database."""
        saved_user_info = User(allergies=self.fa_set, is_vegan=self.dr_dict["Vegan"],
                               is_vegetarian=self.dr_dict["Vegetarian"],
                               is_lactose_intolerant=self.dr_dict["Lactose-free"])

        # add info to database (check with retrieve_user_info)
        self.prepmate_window.database.create_table_allergies()
        self.prepmate_window.database.create_table_dietary_restrictions()
        self.prepmate_window.database.add_user_info(saved_user_info)

        pop_up_saved = QMessageBox()
        pop_up_saved.setWindowTitle('User information updated')
        pop_up_saved.setText('Your selected food allergies and dietary restrictions are saved!')
        pop_up_saved.setStandardButtons(QMessageBox.Ok)     # type: ignore[attr-defined]
        pop_up_saved.exec()

    def eggs_box_toggled(self, checked) -> None:
        """Method saves eggs in the food allergies set when its checkbox toggled,
        and removes it when untoggled."""
        if checked:
            self.fa_set.add('Eggs')
        else:
            self.fa_set.remove('Eggs')

    def milk_box_toggled(self, checked) -> None:
        """Method saves milk in the food allergies set when its checkbox toggled,
        and removes it when untoggled."""
        if checked:
            self.fa_set.add('Milk')
        else:
            self.fa_set.remove('Milk')

    def gluten_box_toggled(self, checked) -> None:
        """Method saves gluten in the food allergies set when its checkbox toggled,
        and removes it when untoggled."""
        if checked:
            self.fa_set.add('Gluten')
        else:
            self.fa_set.remove('Gluten')

    def peanuts_box_toggled(self, checked) -> None:
        """Method saves peanuts in the food allergies set when its checkbox toggled,
        and removes it when untoggled."""
        if checked:
            self.fa_set.add('Peanuts')
        else:
            self.fa_set.remove('Peanuts')

    def fish_box_toggled(self, checked) -> None:
        """Method saves fish in the food allergies set when its checkbox toggled,
        and removes it when untoggled."""
        if checked:
            self.fa_set.add('Fish')
        else:
            self.fa_set.remove('Fish')

    def soybeans_box_toggled(self, checked) -> None:
        """Method saves soybeans in the food allergies set when its checkbox toggled,
        and removes it when untoggled."""
        if checked:
            self.fa_set.add('Soybeans')
        else:
            self.fa_set.remove('Soybeans')

    def lactose_box_toggled(self, checked) -> None:
        """Method saves lactose as a dietary restrictions when its checkbox toggled,
        and removes it when untoggled."""
        if checked:
            self.dr_dict['Lactose-free'] = True
        else:
            self.dr_dict['Lactose-free'] = False

    def vegetarian_box_toggled(self, checked) -> None:
        """Method saves vegetarian as a dietary restrictions when its checkbox toggled,
        and removes it when untoggled."""
        if checked:
            self.dr_dict['Vegetarian'] = True
        else:
            self.dr_dict['Vegetarian'] = False

    def vegan_box_toggled(self, checked) -> None:
        """Method saves vegan as a dietary restrictions when its checkbox toggled,
        and removes it when untoggled."""
        if checked:
            self.dr_dict['Vegan'] = True
        else:
            self.dr_dict['Vegan'] = False
