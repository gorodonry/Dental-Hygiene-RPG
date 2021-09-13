##
# constants.py
# Date: 09/09/2021
# Author: Ryan Gordon
# Contains all the constants for the dental hygiene RPG

# Dictionary of opponents (excl. the final boss), their base health, and level
OPPONENTS = {"Plaque Monster": (55, 2),
             "Holey Tooth": (35, 1),
             "Rotten Tooth": (45, 2),
             "Chipped Tooth": (30, 1),
             "Sugarholic Teeth": (65, 3),
             "Candy Corn": (35, 1),
             "L&P": (25, 1)}

# Dictionary of which level monsters can occur at which stages
STAGES = {1: tuple([1]), 2: (1, 2), 3: tuple([2]), 4: (2, 3)}

# List attacks and opponents that can use them
BAD_BRUSHING_SCHEDULE = tuple(["Sugarholic Teeth"])
CANDY_CORN = ("Candy Corn", "Sugarholic Teeth", "Rotten Tooth")
BAD_BREATH = ("Sugarholic Teeth", "Rotten Tooth", "Plaque Monster")
PLAQUE = ("Plaque Monster", "Sugarholic Teeth", "Rotten Tooth", "Holey Tooth")
SUGAR = ("Sugarholic Teeth", "Candy Corn", "L&P", "Rotten Tooth")
GUM_DISEASE = ("Plaque Monster", "Sugarholic Teeth")
TOFFEE = tuple(["Chipped Tooth"])

# Key order is important when determining attack effectiveness
SPECIFIC_MOB_ATTACKS = {"bad brushing schedule": BAD_BRUSHING_SCHEDULE,
                        "bad breath": BAD_BREATH,
                        "plaque": PLAQUE,
                        "candy corn": CANDY_CORN,
                        "sugar": SUGAR,
                        "gum disease": GUM_DISEASE,
                        "toffee": TOFFEE}

# Messages printed after an attack choice by either the user or opponent
ATTACK_MESSAGES = {"bad brushing schedule": """
They appear to be trying to influence your twice-a-day brushing schedule.""",
                   "bad breath": """
After weeks of no brushing they've developed an incredibly potent breath weapon
 - bleurgh.""",
                   "plaque": """
Millions of bacteria swarm towards you and attack your teeth.""",
                   "candy corn": """
The worst offender - only food by the loosest definition. You can already taste
the sugar as it flies towards you...""",
                   "sugar": """
Aack! The source of all plaque...""",
                   "gum disease": """
It looks like your enemy hasn't been brushing for a while and are turning their
build-up of food on you.""",
                   "toffee": """
A spirited attempt to break your teeth with solid food...""",
                   "blended kale": """
You chuck something healthy at them - this won't damage their teeth!""",
                   "scaler": """
You assail their plaque and try to get rid of it!""",
                   "dental floss": """
You clean their teeth of any food build-ups.""",
                   "toothpaste": """
A staple in dentistry.""",
                   "drill": """
You give your opponent a quick filling. Hopefully that hole should stop growing
now.""",
                   "fluoridated water": """
Much better than whatever they've been drinking... and fortified with fluoride!
You kind of can't go wrong.""",
                   "dental pamphlet": """
The best thing for them is to visit a dentist."""}

# Messages printed after a battle, dependent on opponent
BATTLE_END_MESSAGES = {"Plaque Monster": """
Getting rid of the plaque with a scaler proved immensely successful.""",
                       "Holey Tooth": """
Good job repairing those fillings.""",
                       "Rotten Tooth": """
Removal of the plaque build-up and the prevetion of further decay with fluoride
in the water was an excellent idea.""",
                       "Chipped Tooth": """
The best thing for them was indeed to visit the dentist.""",
                       "Sugarholic Teeth": """
A fearsome enemy - but in the end only the preventative classics toothpaste and
dental floss were necessary.""",
                       "Candy Corn": """
My god that was a lot of sugar. Something healthier would be better...""",
                       "L&P": """
Why would anyone need anything more than water and fluoride?"""}

# Dictionaries of opponent weaknesses and strengths
WEAKNESSES = {"blended kale": tuple(["Candy Corn"]),
              "scaler": ("Plaque Monster", "Rotten Tooth"),
              "dental floss": tuple(["Sugarholic Teeth"]),
              "toothpaste": tuple(["Sugarholic Teeth"]),
              "drill": tuple(["Holey Tooth"]),
              "fluoridated water": ("L&P", "Rotten Tooth", "Sugarholic Teeth"),
              "dental pamphlet": tuple(["Chipped Tooth"])}

STRENGTHS = {"blended kale": ("Rotten Tooth", "Sugarholic Teeth"),
             "scaler": ("Candy Corn", "L&P"),
             "dental floss": ("Holey Tooth", "Chipped Tooth"),
             "toothpaste": ("Holey Tooth", "Chipped Tooth"),
             "drill": ("Candy Corn", "L&P", "Sugarholic Teeth"),
             "fluoridated water": (),
             "dental pamphlet": tuple(["Plaque Monster"])}

# For both the user and the computer opponent
BASE_DAMAGE = 10

# List of possible attack effectiveness used in character creation
AVAILABLE_EFFECTS = (True, True, None, None, None, False, False)

# One of these names is chosen if the user enters '' for a name
NULL_NAMES = ("Nada", "Nothing", "Null", "Zilch", "Naught", "Fred", "Bob",
              "Kat")

# List of three options users can choose from when choosing character traits
VALID_STATS = {"g": "good", "b": "bad", "m": "meh"}

# Used for some user inputs/menus
ALPHABET = tuple("abcdefghijklmnopqrstuvwxyz")
