# pylint: disable=too-few-public-methods
"""This module contains the Ingredient class"""


class Ingredient:
    """This class will be used to create ingredient objects"""
    def __init__(self, name: str, **kwargs) -> None:
        self.name: str = name
        self.quantity: int | None = kwargs.get("quantity", 0)
        self.unit: str | None = kwargs.get("unit", None)
        self.is_vegan: bool | None = kwargs.get('is_vegan', None)
        self.is_vegetarian: bool | None = kwargs.get('is_vegetarian', None)
        self.is_lactose_free: bool | None = kwargs.get('is_lactose_free', None)
