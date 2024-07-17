"""This file contains the tests for the functions in
the test_scale_ingredients.py file."""


import unittest
from project.back_end.scale_ingredients import scale_ingredients
from project.back_end.ingredient import Ingredient


class TestScaleIngredients(unittest.TestCase):
    """The test class for the scale ingredients function."""
    def test_scale_ingredients(self):
        """Test the function scale_ingredients."""
        ingredient_input_1 = Ingredient('Onion', quantity=1, unit='piece')
        ingredient_input_2 = Ingredient('Chicken', quantity=200, unit='g')
        ingredient_input_3 = Ingredient('Potato', quantity=75, unit='g')
        ingredient_output_1 = Ingredient('Onion', quantity=1*4, unit='piece')
        ingredient_output_2 = Ingredient('Chicken', quantity=200*4, unit='g')
        ingredient_output_3 = Ingredient('Potato', quantity=75*4, unit='g')
        ingredients_input = [ingredient_input_1, ingredient_input_2, ingredient_input_3]
        expected_ingredients_output = [
            ingredient_output_1,
            ingredient_output_2,
            ingredient_output_3
        ]
        ingredients_output = scale_ingredients(ingredients_input, 4)
        self.assertEqual(expected_ingredients_output[0].quantity, ingredients_output[0].quantity)
        self.assertEqual(expected_ingredients_output[1].quantity, ingredients_output[1].quantity)
        self.assertEqual(expected_ingredients_output[2].quantity, ingredients_output[2].quantity)


if __name__ == '__main__':
    unittest.main()
