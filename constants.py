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
STAGES = {1: (1,), 2: (1, 2), 3: (2,), 4: (2, 3)}

# List attacks and opponents that can use them
BAD_BRUSHING_SCHEDULE = ("Sugarholic Teeth",)
CANDY_CORN = ("Candy Corn", "Sugarholic Teeth", "Rotten Tooth")
BAD_BREATH = ("Sugarholic Teeth", "Rotten Tooth", "Plaque Monster")
PLAQUE = ("Plaque Monster", "Sugarholic Teeth", "Rotten Tooth", "Holey Tooth")
SUGAR = ("Sugarholic Teeth", "Candy Corn", "L&P", "Rotten Tooth")
GUM_DISEASE = ("Plaque Monster", "Sugarholic Teeth")
TOFFEE = ("Chipped Tooth",)

# Key order is important when determining attack effectiveness
SPECIFIC_MOB_ATTACKS = {"bad brushing schedule": BAD_BRUSHING_SCHEDULE,
                        "bad breath": BAD_BREATH,
                        "plaque": PLAQUE,
                        "candy corn": CANDY_CORN,
                        "sugar": SUGAR,
                        "gum disease": GUM_DISEASE,
                        "toffee": TOFFEE}

# Information about the effect of certain user attacks, .split() at asterisks
ATTACK_HELP = {"blended kale": """
Blended kale (/blɛndɪd keɪl/, noun, pl. blended kale)*
Food can't get much better for your teeth than this. Way better than candy corn
that's for sure. Encourage your patients to eat this whenever possible.""",
               "scaler": """
Scaler (/skeɪlɑ/, noun, pl. scalers)*
Your patients probably know this as 'the scrapey tool'. We know it simply can't
be beaten when it comes to getting rid of plaque buildups.""",
               "dental floss": """
Dental floss (/ˈdɛnt(ə)l flɒs/, noun, pl. dental floss)*
Not many people use this nowadays, but its power isn't to be underestimated all
the same. Looks like tough green string, very good for clearing stuck food from
between your teeth. Recommend patients use daily, night is best. A preventative
measure up there with toothpaste. Rumour has it it's most effective against any
teeth not yet feeling the consequences of a sugary diet.""",
               "toothpaste": """
Toothpaste (/ˈtuːθpeɪst/, noun, pl. toothpastes)*
Used twice a day, emphasis on night. Brush teeth with it to get rid of constant
film of plaque that forms on teeth. A preventative measure most useful for foes
not currently experiencing tooth decay, but about to.""",
               "drill": """
Drill (/drɪl/, noun, pl. drills)*
Used for cutting away part of a tooth prior to filling it. Local anaesthetic is
recommended, but not necessary.""",
               "fluoridated water": """
Fluoridated water (/ˈflʊərɪdeɪtɪd ˈwɔːtə/, noun, pl. fluoridated water)*
Drinking water laced with fluoride. Present in most towns and cities of NZ with
exceptions rapidly disappearing. The simplest preventative measure there is for
tooth decay, people don't even notice it's there. Good for everything.""",
               "dental pamphlet": """
Dental pamphlet (/ˈdɛnt(ə)l ˈpamflɪt/, noun, pl. dental pamphlets)*
Some things are just too hard to cure on the spot. Like broken teeth. Direct to
a dentist with a studio ASAP."""}

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
You chuck something healthy at them - far better than what they're eating!""",
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
Good job repairing those fillings with that drill.""",
                       "Rotten Tooth": """
Removing their plaque with a scaler and converting them to fluoridated water is
the way to go!""",
                       "Chipped Tooth": """
The best thing for them was to visit a dentist. Only so much you can do without
the proper equipment...""",
                       "Sugarholic Teeth": """
A fearsome enemy - one convinced that sugar is amazing, but not yet feeling the
consequences... the preventative measures toothpaste and dental floss proved to
be a success.""",
                       "Candy Corn": """
My god that was a lot of sugar. Something healthier would be better...""",
                       "L&P": """
Why would anyone need anything more than water and fluoride..?"""}

# Dictionaries of opponent weaknesses and strengths
WEAKNESSES = {"blended kale": ("Candy Corn",),
              "scaler": ("Plaque Monster", "Rotten Tooth"),
              "dental floss": ("Sugarholic Teeth",),
              "toothpaste": ("Sugarholic Teeth",),
              "drill": ("Holey Tooth",),
              "fluoridated water": ("L&P", "Rotten Tooth", "Sugarholic Teeth"),
              "dental pamphlet": ("Chipped Tooth",)}

STRENGTHS = {"blended kale": ("Rotten Tooth", "Sugarholic Teeth"),
             "scaler": ("Candy Corn", "L&P"),
             "dental floss": ("Holey Tooth", "Chipped Tooth"),
             "toothpaste": ("Holey Tooth", "Chipped Tooth"),
             "drill": ("Candy Corn", "L&P", "Sugarholic Teeth"),
             "fluoridated water": (),
             "dental pamphlet": ("Plaque Monster",)}

# For both the user and the computer opponent
BASE_DAMAGE = 10

# List of possible attack effectiveness used in character creation
AVAILABLE_EFFECTS = (True, True, None, None, None, False, False)

# One of these names is chosen if the user enters '' for a name
NULL_NAMES = ("Nada", "Nothing", "Null", "Zilch", "Naught", "Fred", "Bob",
              "Kat", "Spode", "Ogg", "Mabel", "Arthur", "Trevor")

# List of three options users can choose from when choosing character traits
VALID_STATS = {"g": "good", "b": "bad", "m": "meh"}

# Valid route choices during the game
FOREST_ROUTES = {"1": "main road", "2": "fens"}
