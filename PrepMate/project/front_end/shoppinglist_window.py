"""
This module contains the ShoppingListWindow class, a widget that
displays the shopping list.
"""


from typing import TYPE_CHECKING
from PySide6.QtWidgets import (QGroupBox, QCheckBox, QPushButton, QWidget, QVBoxLayout,
                               QScrollArea, QHBoxLayout, QGridLayout, QLabel, QComboBox,
                               QLineEdit, QSpinBox, QLayout)
from PySide6.QtCore import Qt
from project.back_end.ingredient import Ingredient
if TYPE_CHECKING:
    from project.__main__ import PrepMateWindow


class ShoppingListWindow(QWidget):
    """
    QWidget for displaying the shopping list.
    """
    def __init__(self, prepmate_window: "PrepMateWindow") -> None:
        super().__init__()
        self.add_item_window = None
        self.prepmate_window = prepmate_window
        # This will be a list of pairs, connecting an QCheckbox with an Ingredient object
        # (shoppinglist item). Would have preferred a dictionary, since this is only necessary for
        # looking up an ingredient when a checkbox is toggled, but QCheckboxes aren't hashable.

        # Layout: create the list
        self.list_layout = self.create_list_layout()
        group_box = QGroupBox("My Shopping List")
        group_box.setLayout(self.list_layout)

        # Layout: create the buttons
        button_back_to_main = QPushButton("Back to Main Menu")
        button_back_to_main.clicked.connect(prepmate_window.to_mainmenuwindow)
        button_select_all = QPushButton("Select All Items")
        button_select_all.clicked.connect(self.select_all)
        button_add_item = QPushButton("Add Item")
        button_add_item.clicked.connect(self.create_add_item_window)
        button_delete_items = QPushButton("Remove")
        button_delete_items.clicked.connect(lambda: self.remove_selected_items(self))

        # Layout: add everything together
        line_of_buttons_layout = QHBoxLayout()
        line_of_buttons_layout.addWidget(button_select_all)
        line_of_buttons_layout.addWidget(button_add_item)
        outer_layout = QVBoxLayout()
        outer_layout.addWidget(button_back_to_main)
        outer_layout.addLayout(line_of_buttons_layout)
        outer_layout.addWidget(group_box)
        outer_layout.addWidget(button_delete_items)
        widget = QWidget()
        widget.setLayout(outer_layout)

        # Layout: add the scroll area
        self.shopping_scroll = QScrollArea()
        self.shopping_scroll.setVerticalScrollBarPolicy(Qt.ScrollBarPolicy.ScrollBarAlwaysOn)
        self.shopping_scroll.setHorizontalScrollBarPolicy(Qt.ScrollBarPolicy.ScrollBarAlwaysOff)
        self.shopping_scroll.setWidgetResizable(True)
        self.shopping_scroll.setWidget(widget)

    def create_list_layout(self) -> QLayout:
        """
        Method to create a layout containing all the shopping list items as checkboxes.
        It also creates a list linking the Ingredient with a QCheckbox, which can
        be used to delete items.
        """
        layout = QVBoxLayout()

        self.checkbox_to_ingredient = []
        lst_of_items = self.prepmate_window.database.retrieve_shopping_list()
        for item in lst_of_items:
            new_checkbox = self.create_item_checkbox(item)
            layout.addWidget(new_checkbox)
            self.checkbox_to_ingredient += [[new_checkbox, item]]
        return layout

    @staticmethod
    def create_item_checkbox(item: "Ingredient") -> QCheckBox:
        """
        -> create_item_checkbox(Ingredient)
        Method to create a single checkbox for the shopping list.
        Can be changed depending on the form of the data from the database.
        """
        return QCheckBox(f"{item.quantity} {item.unit} {item.name}")

    @staticmethod
    def remove_selected_items(shoppinglst_wdgt) -> None:
        """This method will remove the selected items from the shopping list."""
        new_checkbox_to_ingredient = []
        for checkbox, item in shoppinglst_wdgt.checkbox_to_ingredient:
            if checkbox.isChecked():
                shoppinglst_wdgt.list_layout.removeWidget(checkbox)
                checkbox.deleteLater()
                shoppinglst_wdgt.prepmate_window.database.delete_ingredient_from_shopping_list(item)
            else:
                new_checkbox_to_ingredient += [[checkbox, item]]
        shoppinglst_wdgt.checkbox_to_ingredient = new_checkbox_to_ingredient

    def select_all(self) -> None:
        """This method checks all the checkboxes in the shopping list."""
        for checkbox_item in self.checkbox_to_ingredient:
            checkbox_item[0].setChecked(True)

    def create_add_item_window(self):
        """This method opens an AddItem window, where the user can add a new shopping list item."""
        self.add_item_window = AddItemWindow(self)
        self.add_item_window.show()

    def add_item_to_list(self, new_ingredient) -> None:
        """This method adds the user's new ingredient to the shopping list."""
        self.prepmate_window.database.add_ingredient_to_shopping_list(new_ingredient)
        # refresh the list by recreating the widget:
        self.prepmate_window.to_shoppinglistwindow()


class AddItemWindow(QWidget):
    """This class represents the window that pops up when
    a user wants to add an item to the shopping list manually"""
    def __init__(self, shoppinglist_window) -> None:
        super().__init__()
        self.shoppinglist_window = shoppinglist_window
        self.setWindowTitle("Add Item to Shopping List")
        self.setGeometry(610, 300, 400, 200)

        label_name = QLabel("Enter ingredient name:")
        label_unit = QLabel("Select unit:")
        label_quantity = QLabel("Enter quantity:")

        self.lineedit_name = QLineEdit()
        self.combobox_unit = QComboBox()
        self.spinbox_quantity = QSpinBox()

        self.spinbox_quantity.setMaximum(99999)
        self.combobox_unit.addItem("g")
        self.combobox_unit.addItem("ml")
        self.combobox_unit.addItem("piece")

        add_button = QPushButton("Add ingredient to shopping list")
        add_button.clicked.connect(self.added_item)

        layout = QGridLayout()
        layout.addWidget(label_name, 0, 0)
        layout.addWidget(label_unit, 1, 0)
        layout.addWidget(label_quantity, 2, 0)
        layout.addWidget(self.lineedit_name, 0, 1, 1, 2)
        layout.addWidget(self.combobox_unit, 1, 1, 1, 2)
        layout.addWidget(self.spinbox_quantity, 2, 1, 1, 2)
        layout.addWidget(add_button, 3, 0, 1, 3)
        self.setLayout(layout)

    def added_item(self) -> None:
        """This method creates an ingredient from the user's input, and
        passes it back to the ShoppingListWindow before closing the AddItemWindow"""
        new_ingredient_name = self.lineedit_name.text().strip().capitalize()
        new_ingredient_unit = self.combobox_unit.currentText()
        new_ingredient_quantity = self.spinbox_quantity.value()
        new_ingredient = Ingredient(new_ingredient_name,
                                    unit=new_ingredient_unit,
                                    quantity=new_ingredient_quantity)
        self.shoppinglist_window.add_item_to_list(new_ingredient)
        self.close()
