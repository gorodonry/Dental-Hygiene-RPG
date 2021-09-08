##
# dentist_rpg_v3.py
# Date: 06/09/2021
# Author: Ryan Gordon
# Plays an RPG game with the user as a dentist, promotes good dental hygiene

'''
Version 3

Contains the opponent and player classes transferred from version 2, as well as
the various constants used to create those classes. Also contains the game
situation which is printed to the user and the relevant functions for that.

New to version 3 are the various statistics the user's character has which are
necessary for the battle sequence. These statistics are coded into the player
class or as constants.
'''

import random
from math import ceil
from time import sleep


def get_stat(prompt, stats):
    """
    Asks user for a character stat and returns the answer.

    A character stat (e.g. self discipline, agility) is entered as either good,
    bad, or meh.
    """
    ans = ""
    while ans not in VALID_STATS or (stats.count(ans) == 2 and ans != "meh"):
        ans = input(prompt).strip().lower()
        if ans not in VALID_STATS:
            print("Does that really look like one of the options to you?")
        # Users cannot be either good or bad at everything
        elif stats.count(ans) == 2 and ans != "meh":
            print(f"You can't be {ans} at everything!")
    return ans


def get_effect(available, stat=None):
    """
    Randomly determines the effectiveness of an opponent attack.

    Used as part of character creation (after the characteristics have been
    entered by the user).
    """
    if stat is None:
        return random.choice(available)
    elif stat == "good" and True in available:
        return True
    elif stat == "bad" and False in available:
        return False
    elif None in available:
        return None
    else:
        return random.choice(available)


def print_slow(message, newline='\n'):
    """
    Prints a line one character at a time.

    Used to enhance user experience while playing the game.
    """
    for character in list(message):
        print(character, end='')
        sleep(0.01)
    print(end=newline)


class Opponent:
    """Creates an opponent object."""

    def __init__(self, stage):
        """
        Basic setup and variables for the computer opponent.

        param stage (int): battle the player is up to, determines available
        opponents when choosing an opponent and slightly increases opponent
        health with each stage.
        """

        # Determine opponent randomly based off the stage
        available_levels, available_opponents = STAGES[stage], []
        for opponent in OPPONENTS:
            if OPPONENTS[opponent][1] in available_levels:
                available_opponents.append(opponent)
        self.name = random.choice(available_opponents)

        # Determine health with a random component
        base_health = OPPONENTS[self.name][0]
        self.health = random.randint(base_health - 5, base_health + 5)
        # The more battles the user fights, the higher the health, also random
        self.health += ceil(random.randint(stage - 1, stage + 2) * 1.5)

        # Determine available attacks based off the chosen opponent
        self.attacks = []
        for attack in AVAILABLE_MOB_ATTACKS:
            if self.name in AVAILABLE_MOB_ATTACKS[attack]:
                self.attacks.append(attack)

    def add_attack(self, attack):
        """Adds a new attack to an opponent."""
        self.attacks.append(attack)

    def get_attack(self):
        """Chooses a random attack and returns it."""
        return random.choice(self.attacks)

    def get_status(self):
        """Returns True if alive, False is dead."""
        return self.health > 0

    def take_damage(self, damage):
        """Reduces health based on user damage."""
        self.health -= damage


class Player:
    """Creates an object that contains all the player's information."""

    def __init__(self):
        """Initial setup of character."""
        # Start of character creation messages
        print_slow("Greetings applicant", '\n\n')
        sleep(1)
        print_slow("We need some information about you.", '\n\n')
        sleep(1)

        print("Guild application form\n")

        # Get player name
        self.name = input("Name: ").strip()
        if self.name == "":
            self.name = random.choice(NULL_NAMES)

        # Get self discipline, agility, and teeth strength as good/bad/meh
        self.stats = {}
        prompt = "How good is your self discipline (good/bad/meh)? "
        self_discipline = get_stat(prompt, list(self.stats.values()))
        self.stats["self discipline"] = self_discipline
        prompt = "How good is your agility (good/bad/meh)? "
        agility = get_stat(prompt, list(self.stats.values()))
        self.stats["agility"] = agility
        prompt = "Lastly, how healthy are your teeth (good/bad/meh)? "
        teeth_strength = get_stat(prompt, list(self.stats.values()))
        self.stats["teeth strength"] = teeth_strength

        print()
        print_slow("Thank you. ", '')
        sleep(1)
        print_slow("But this is just writing. ", '')
        sleep(1)
        print_slow("""Prior to joining you must undergo a series of tests.""")
        sleep(1)
        print()
        print_slow("The assessor shows you another door and steps back. ", '')
        sleep(1)
        print_slow("You open it...")

        # End of character creation messages, create any remaining user vars

        # Use the traits to psuedo-randomly determine attack effectiveness
        effects, self.affected_by = list(AVAILABLE_EFFECTS), {}
        attacks = list(SPECIFIC_MOB_ATTACKS.keys())
        # Give each opponent attack an effectiveness rating against the user
        for attack in range(len(effects)):
            # Effect aka relative damage (True: high, False: low, None: usual)
            try:
                # The first three are based off character stats
                stat = list(self.stats.values())[attack]
                self.affected_by[attacks[attack]] = get_effect(effects, stat)
            except IndexError:
                # The rest are determined randomly based on what's left
                self.affected_by[attacks[attack]] = get_effect(effects)
            # Remove the chosen effect from the remaining effects to dole out
            effects.remove(list(self.affected_by.values())[-1])

        # Set up hit points
        self.max_health = 35
        self.health = self.max_health

        # User starts out with attacks effective against L1 monsters
        self.attacks = []
        for opponent, stats in OPPONENTS.items():
            if stats[1] == 1:
                for weakness in WEAKNESSES:
                    if opponent in WEAKNESSES[weakness]:
                        self.attacks.append(weakness)

    def add_attack(self, attack):
        """Adds a new attack to the player's arsenal."""
        self.attacks.append(attack)

    def get_status(self):
        """Returns True if alive, False is dead."""
        return self.health > 0

    def take_damage(self, damage):
        """Reduces health based on opponent damage."""
        self.health -= damage

    def heal(self, amount):
        """Increases health by specified amount (up to the max)."""
        if self.health + amount >= self.max_health:
            self.health = self.max_health
        else:
            self.health += amount

    def heal_full(self):
        """Restores user to max health."""
        self.health = self.max_health

    def increase_max_health(self, amount):
        """Increases max health by specified amount."""
        self.max_health += amount


def print_prelude():
    """Prints the prelude to the game."""
    print("Dental Hygiene RPG".center(80))
    print_slow("""
You walk up the dark, empty street and turn left. """, '')
    sleep(1)
    print_slow("Another dark alleyway.")
    sleep(1)
    print_slow("""
The kingdom hasn't been the same lately; """, '')
    sleep(1)
    print_slow("""rumours of a great evil roaming across
the land have been circulating. """, '')
    sleep(1)
    print_slow("Rumours that seem to be becoming fact...")
    sleep(1)
    print()
    print_slow("That's why you're here, after all.")
    sleep(1)
    print_slow("""
The mist stirs ahead of you... and suddenly you can see it - """, '')
    sleep(1)
    print_slow("""a small wood door,
nondescript bar the insignia scratched into its surface. """)
    sleep(1)
    print()
    print_slow("Your heartrate increases as you knock on it...")
    sleep(1)
    print("\n")

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
BASE_ATTACK_DAMAGE = 10

# List of possible attack effectiveness used in character creation
AVAILABLE_EFFECTS = (True, True, None, None, None, False, False)

# One of these names is chosen if the user enters '' for a name
NULL_NAMES = ("Nada", "Nothing", "Null", "Zilch", "Naught")

# List of three options users can choose from when choosing character traits
VALID_STATS = ("good", "bad", "meh")

if __name__ == "__main__":
    # Print prelude to character creation, then create the character
    print_prelude()
    user = Player()
