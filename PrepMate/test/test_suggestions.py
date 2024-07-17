"""This test suite will be used to test the back-end of the PrepMate application"""

# Imports from this project
from project.back_end.recipe_suggestions import Suggestions
from project.back_end.user import User
from project.back_end.recipe import Recipe
from project.back_end.ingredient import Ingredient

# All ingredients for testing
chicken_nuggets = Ingredient(name="Chicken nuggets",
                             is_vegetarian=False, is_vegan=False, is_lactose_free=False)
fries = Ingredient(name="Fries",
                   is_vegetarian=True, is_vegan=True, is_lactose_free=True)
eggs = Ingredient(name="Eggs",
                  is_vegan=False, is_vegetarian=True, is_lactose_free=True)
milk = Ingredient(name="Milk",
                  is_vegan=False, is_vegetarian=True, is_lactose_free=False)
flour = Ingredient(name="Flour",
                   is_vegan=True, is_vegetarian=True, is_lactose_free=True)
peanuts = Ingredient(name="Peanuts",
                     is_vegan=True, is_vegetarian=True, is_lactose_free=True)
rice_noodles = Ingredient(name="Rice noodles",
                          is_vegan=True, is_vegetarian=True, is_lactose_free=True)
shrimps = Ingredient(name="Shrimps",
                     is_vegan=False, is_vegetarian=False, is_lactose_free=True)
soy_sauce = Ingredient(name="Soy sauce",
                       is_vegan=True, is_vegetarian=True, is_lactose_free=True)
spring_onions = Ingredient(name="Spring onions",
                           is_vegan=True, is_vegetarian=True, is_lactose_free=True)
pasta = Ingredient(name="Pasta",
                   is_vegan=True, is_vegetarian=True, is_lactose_free=True)
onion = Ingredient(name="Onion",
                   is_vegan=True, is_vegetarian=True, is_lactose_free=True)
cellery = Ingredient(name="Cellery",
                     is_vegan=True, is_vegetarian=True, is_lactose_free=True)
carrots = Ingredient(name="Carrots",
                     is_vegan=True, is_vegetarian=True, is_lactose_free=True)
stock = Ingredient(name="Stock",
                   is_vegan=True, is_vegetarian=True, is_lactose_free=True)
red_wine = Ingredient(name="Red_wine",
                      is_vegan=True, is_vegetarian=True, is_lactose_free=True)
ground_beef = Ingredient(name="Ground beef",
                         is_vegan=False, is_vegetarian=False, is_lactose_free=True)
arugula = Ingredient(name="Arugula",
                     is_vegan=True, is_vegetarian=True, is_lactose_free=True)
tomatoes = Ingredient(name="Tomatoes",
                      is_vegan=True, is_vegetarian=True, is_lactose_free=True)
balsamic_vinegar = Ingredient(name="Balsamic vinegar",
                              is_vegan=True, is_vegetarian=True, is_lactose_free=True)

# All recipes for testing
fries_and_nuggets = Recipe(name="Fries and nuggets",
                           ingredients=[chicken_nuggets, fries],
                           calories=100,
                           prep_time=20)
scramled_eggs = Recipe(name="Scrambled eggs", # GONE
                       ingredients=[eggs],
                       calories=900,
                       prep_time=60)
pancakes = Recipe(name="Pancakes",
                  ingredients=[eggs, flour, milk],
                  calories=400,
                  prep_time=90)
pad_thai = Recipe(name="Pad thai", # GONE
                  ingredients=[peanuts, rice_noodles, shrimps, soy_sauce, spring_onions],
                  calories=10,
                  prep_time=100)
ragu_bolognese = Recipe(name="Ragu bolognese",
                        ingredients=[
                            pasta, onion, cellery, carrots, stock, red_wine, ground_beef
                        ],
                        calories=750,
                        prep_time=10)
italian_salad = Recipe(name="Salad", # GONE
                       ingredients=[arugula, tomatoes, balsamic_vinegar],
                       calories=625,
                       prep_time=30)


def test_suggestions_1() -> None:
    """This test will check if the vegan filter works in the Suggestions class"""
    vegan_user = User(is_vegan=True)
    suggestions1 = Suggestions(user=vegan_user, recipes=[fries_and_nuggets])
    assert not suggestions1.filtered_recipes


def test_suggestions_2() -> None:
    """This test will check if the vegetarian filter works in the Suggesitions class"""
    vegetarian_user = User(is_vegetarian=True)
    suggestions2 = Suggestions(user=vegetarian_user, recipes=[scramled_eggs])
    assert suggestions2.filtered_recipes == [scramled_eggs]


def test_suggestions_3() -> None:
    """This test will check if the lactose intolerant filter works in the Suggestions class"""
    lactose_intolerant_user = User(is_lactose_intolerant=True)
    suggestions3 = Suggestions(user=lactose_intolerant_user, recipes=[pancakes])
    assert not suggestions3.filtered_recipes


def test_suggestions_4() -> None:
    """This test will check if the allergy filter works in the Suggestions class"""
    peanut_allergic_user = User(allergies=['Peanuts'])
    suggestions4 = Suggestions(user=peanut_allergic_user, recipes=[pad_thai])
    assert not suggestions4.filtered_recipes


def test_suggestions_5() -> None:
    """This test will check if the allergy filter works in the Suggestions class"""
    multiple_allergy_person = User(allergies=['Pasta', 'Cellery'])
    suggestions5 = Suggestions(user=multiple_allergy_person, recipes=[ragu_bolognese])
    assert not suggestions5.filtered_recipes


def test_suggestions_6() -> None:
    """
    This test will check if the allergy filter works in combination with the vegan filter
    in the Suggestions class
    """
    allergy_vegan_person = User(is_vegan=True, allergies=['Peanuts'])
    suggestions6 = Suggestions(user=allergy_vegan_person,
                               recipes=[
                                   fries_and_nuggets,
                                   scramled_eggs,
                                   pancakes,
                                   italian_salad,
                                   pad_thai,
                                   ragu_bolognese
                               ])
    assert suggestions6.filtered_recipes == [italian_salad]


def test_random_1() -> None:
    """This test will check if the random_suggestions method works in the Suggestions class"""
    random_user = User()
    suggestions1 = Suggestions(user=random_user,
                               recipes=[
                                   fries_and_nuggets,
                                   scramled_eggs,
                                   pancakes,
                                   italian_salad,
                                   pad_thai,
                                   ragu_bolognese
                               ])
    suggestions1.random_suggestions()
    assert len(suggestions1.suggestions) == 6


def test_random_2() -> None:
    """
    This test will check if the random_suggestions method works in the Suggestions
    class in combination with the vegan filter
    """
    random_vegan = User(is_vegan=True)
    suggestions2 = Suggestions(user=random_vegan,
                               recipes=[
                                   fries_and_nuggets,
                                   scramled_eggs,
                                   pancakes,
                                   italian_salad,
                                   pad_thai,
                                   ragu_bolognese
                               ])
    suggestions2.random_suggestions()
    assert len(suggestions2.suggestions) == 1


def test_random_3_double_suggestion() -> None:
    """This test will check if the random_suggestions method works if the method is called twice"""
    random_user = User()
    suggestions3 = Suggestions(user=random_user,
                               recipes=[
                                   fries_and_nuggets,
                                   scramled_eggs,
                                   pancakes,
                                   italian_salad,
                                   pad_thai,
                                   ragu_bolognese
                               ])
    suggestions3.random_suggestions()
    suggestions3.random_suggestions()
    assert len(suggestions3.suggestions) == 0


def test_check_user_preferences_cooking_time_given():
    """This test checks if the check_user_preferences method filters correctly
    when the user inputs a maximum preparation time."""
    random_user = User()
    user_preferences = [[], [], None, 30]
    suggestions = Suggestions(user=random_user,
                              recipes=[
                                  fries_and_nuggets,
                                  scramled_eggs,
                                  pancakes,
                                  italian_salad,
                                  pad_thai,
                                  ragu_bolognese
                              ])
    suggestions.check_user_preferences(*user_preferences)
    assert suggestions.filtered_recipes == [fries_and_nuggets,
                                            italian_salad,
                                            ragu_bolognese]


def test_check_user_preferences_no_preferences_given():
    """This test checks if the check_user_preferences method does not filter
    if no preferences are given"""
    random_user = User()
    user_preferences = [[], [], None, None]
    suggestions = Suggestions(user=random_user,
                              recipes=[
                                  fries_and_nuggets,
                                  scramled_eggs,
                                  pancakes,
                                  italian_salad,
                                  pad_thai,
                                  ragu_bolognese
                              ])
    suggestions.check_user_preferences(*user_preferences)
    assert suggestions.filtered_recipes == [fries_and_nuggets,
                                            scramled_eggs,
                                            pancakes,
                                            italian_salad,
                                            pad_thai,
                                            ragu_bolognese]


def test_check_user_preferences_calorierange():
    """This test checks if the check_user_preferences method filters correctly
    when the user inputs a range of preferred calories."""
    random_user = User()
    user_preferences = [[], [], (500, 1500), None]
    suggestions = Suggestions(user=random_user,
                              recipes=[
                                  fries_and_nuggets,
                                  scramled_eggs,
                                  pancakes,
                                  italian_salad,
                                  pad_thai,
                                  ragu_bolognese
                              ])
    suggestions.check_user_preferences(*user_preferences)
    assert suggestions.filtered_recipes == [scramled_eggs,
                                            italian_salad,
                                            ragu_bolognese]


def test_check_user_preferences_single_musthave():
    """This test checks if the check_user_preferences method filters correctly
    when the user inputs one must-have ingredient."""
    random_user = User()
    user_preferences = [["Eggs"], [], None, None]
    suggestions = Suggestions(user=random_user,
                              recipes=[
                                  fries_and_nuggets,
                                  scramled_eggs,
                                  pancakes,
                                  italian_salad,
                                  pad_thai,
                                  ragu_bolognese
                              ])
    suggestions.check_user_preferences(*user_preferences)
    assert suggestions.filtered_recipes == [scramled_eggs,
                                            pancakes]


def test_check_user_preferences_double_musthave():
    """This test checks if the check_user_preferences method filters correctly
    when the user inputs two must-have ingredients."""
    random_user = User()
    user_preferences = [["Eggs", "Milk"], [], None, None]
    suggestions = Suggestions(user=random_user,
                              recipes=[
                                  fries_and_nuggets,
                                  scramled_eggs,
                                  pancakes,
                                  italian_salad,
                                  pad_thai,
                                  ragu_bolognese
                              ])
    suggestions.check_user_preferences(*user_preferences)
    assert suggestions.filtered_recipes == [pancakes]


def test_check_user_preferences_single_canthave():
    """This test checks if the check_user_preferences method filters correctly
        when the user inputs one can't-have ingredient."""
    random_user = User()
    user_preferences = [[], ["Eggs"], None, None]
    suggestions = Suggestions(user=random_user,
                              recipes=[
                                  fries_and_nuggets,
                                  scramled_eggs,
                                  pancakes,
                                  italian_salad,
                                  pad_thai,
                                  ragu_bolognese
                              ])
    suggestions.check_user_preferences(*user_preferences)
    assert suggestions.filtered_recipes == [fries_and_nuggets,
                                            italian_salad,
                                            pad_thai,
                                            ragu_bolognese]


def test_check_user_preferences_double_canthave():
    """This test checks if the check_user_preferences method filters correctly
        when the user inputs two must-have ingredients."""
    random_user = User()
    user_preferences = [[], ["Eggs", "Tomatoes"], None, None]
    suggestions = Suggestions(user=random_user,
                              recipes=[
                                  fries_and_nuggets,
                                  scramled_eggs,
                                  pancakes,
                                  italian_salad,
                                  pad_thai,
                                  ragu_bolognese
                              ])
    suggestions.check_user_preferences(*user_preferences)
    assert suggestions.filtered_recipes == [
                                  fries_and_nuggets,
                                  pad_thai,
                                  ragu_bolognese
                              ]


def test_check_user_preferences_multiple_preferences():
    """This test checks if the check_user_preferences method filters correctly
    when the user inputs multiple preferences"""
    # Each input preference removes one recipe
    random_user = User()
    user_preferences = [[], ["Tomatoes"], (0, 850), 90]
    suggestions = Suggestions(user=random_user,
                              recipes=[
                                  fries_and_nuggets,
                                  scramled_eggs,  # calories: 900
                                  pancakes,
                                  italian_salad,  # contains "Tomatoes"
                                  pad_thai,  # Prep time: 100
                                  ragu_bolognese
                              ])
    suggestions.check_user_preferences(*user_preferences)
    assert suggestions.filtered_recipes == [
                                    fries_and_nuggets,
                                    pancakes,
                                    ragu_bolognese
    ]
