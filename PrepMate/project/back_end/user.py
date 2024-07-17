# pylint: disable=too-few-public-methods
"""This module contains the User class"""""

class User():
    """The user class can be used to store user information"""
    def __init__(self, **kwargs) -> None:
        self.is_vegan: bool = kwargs.get("is_vegan", False)
        self.is_vegetarian: bool = kwargs.get("is_vegetarian", False)
        self.is_lactose_intolerant: bool = kwargs.get("is_lactose_intolerant", False)
        self.allergies: set[str] = kwargs.get("allergies", [])
