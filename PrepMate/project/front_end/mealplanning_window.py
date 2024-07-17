"""This module sets up the widget for the meal planning window."""

from PySide6.QtWidgets import (QWidget, QVBoxLayout, QHBoxLayout, QTextEdit,
                               QPushButton, QCalendarWidget, QGroupBox)
from PySide6.QtCore import QDate


class MealPlanningWindow(QWidget):
    """This class generates a window for the meal planning calendar."""
    def __init__(self, prepmate_window) -> None:
        super().__init__()
        self.prepmate_window = prepmate_window
        self.prepmate_window.database.create_table_meal_plans()   # makes the meal_plans table
        self.button_back_to_main = QPushButton("Back to Main Menu")
        self.button_back_to_main.clicked.connect(self.prepmate_window.to_mainmenuwindow)

        self.calendar = QCalendarWidget()
        self.date_min = QDate.currentDate()
        self.date_max = QDate.currentDate().addDays(7)
        self.calendar.setDateRange(self.date_min, self.date_max)
        self.calendar.setVerticalHeaderFormat(
            QCalendarWidget.NoVerticalHeader)   # type: ignore[attr-defined]
        self.calendar.selectionChanged.connect(self.day_selected)

        self.meal_text = QTextEdit()
        self.meal_text.setReadOnly(True)
        self.meal_text.setText('Select a date to view your planned meals.')

        self.set_layout()

    def set_layout(self) -> None:
        """Sets the layout for the meal planning window."""
        # group box
        meal_plan_gb = QGroupBox('Meal Planning Calendar')
        gb_layout = QHBoxLayout()
        gb_layout.addWidget(self.calendar)
        gb_layout.addWidget(self.meal_text)
        meal_plan_gb.setLayout(gb_layout)

        # final layout meal plan window
        layout = QVBoxLayout(self)
        layout.addWidget(self.button_back_to_main)
        layout.addWidget(meal_plan_gb)

    def day_selected(self) -> None:
        """Displays the selected date in the textbox and saved it in the database."""
        self.meal_text.undo()
        date_str = (f'{self.calendar.selectedDate().day()}-{self.calendar.selectedDate().month()}-'
                    f'{self.calendar.selectedDate().year()}')
        retrieved_date = self.prepmate_window.database.retrieve_planned_meal(date_str)
        self.meal_text.setText(f'Your meals for {date_str}: {retrieved_date}')
