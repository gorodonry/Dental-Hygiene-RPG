##
# player_creation_option_3.py
# Date: 02/09/2021
# Author: Ryan Gordon
# Option 3 of dental RPG for the character creation interface

'''
Player creation option 3

Third option for the interface that lets users design their character (with
very limited design features). This option approaches the interface from an
education and sugar perspective and takes trait inputs as integers between 1
and 20, like option 1. Also different from options 1 and 2 here is that the
blocks of text are printed as one block, rather than slowly.
'''

import random
from time import sleep


def get_stat(prompt):
    """
    Asks user for a character stat and returns the answer.

    A character stat (e.g. self discipline, agility) is entered as a number
    between 0 and 20 (inclusive).
    """
    answer = -1
    while answer < 0 or answer > 20:
        try:
            answer = int(input(prompt))
            if answer < 0:
                print("That isn't between 0 and 20.")
            elif answer > 20:
                print("That isn't between 0 and 20.")
        except ValueError:
            print("That isn't even a number.")
    return answer


def get_effect(available, stat=None):
    """
    Randomly determines the effectiveness of an opponent attack.

    Used as part of character creation (after the characteristics have been
    entered by the user).
    """
    if stat is None:
        return random.choice(available)
    elif stat > 15 and True in available:
        return True
    elif stat < 5 and False in available:
        return False
    elif None in available:
        return None
    else:
        return random.choice(available)


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

        # Get player name
        self.name = input("Enter your name: ").strip()
        if self.name == "":
            self.name = random.choice(NULL_NAMES)

        # Get self discipline, agility, and teeth strength as ints between 0&20
        print("\nNow a few random stats")
        self.sd = get_stat("Rank your self discipline (0-20): ")
        self.agility = get_stat("Rank your agility (0-20): ")
        self.teeth_str = get_stat("Lastly, how strong are your teeth (0-20)? ")

        # Use the three traits to randomly determine attack effectiveness
        available_effects, self.effects = list(AVAILABLE_EFFECTS), []
        stats = [self.sd, self.agility, self.teeth_str]
        # Give each opponent attack an effectiveness rating against the user
        for attack in range(len(available_effects)):
            try:
                # The first three are based off character stats
                stat = stats[attack]
                self.effects.append(get_effect(available_effects, stat))
            except IndexError:
                # The rest are determined randomly based on what's left
                self.effects.append(get_effect(available_effects))
            available_effects.remove(self.effects[-1])

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

# List of possible attack effectiveness used in character creation
AVAILABLE_EFFECTS = (True, True, None, None, None, False, False)

# One of these names is chosen if the user enters '' for a name
NULL_NAMES = ("Nada", "Nothing", "Null", "Zilch", "Naught")

if __name__ == "__main__":
    # Print prelude to character creation, then create the character
    print("Dental Hygiene RPG".center(80))
    print("""
Sugar - arguably one of the finest creations in history (if I'm allowed to call
it a creation). It's the source of all our energy... and it tastes really good.
But what does it do to our teeth? Why do dentists constantly tell us off?

Let's take a look...

""")
    user = Player()
    # Determine relative attack damage (True - low, False - high, None - usual)
    attack_effectiveness, attacks = {}, list(SPECIFIC_MOB_ATTACKS.keys())
    for attack in range(7):
        attack_effectiveness[attacks[attack]] = user.effects[attack]
