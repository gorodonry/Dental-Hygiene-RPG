##
# player_creation_option_2.py
# Date: 01/09/2021
# Author: Ryan Gordon
# Option 2 of dental RPG for the character creation interface

'''
Player creation option 2

Second option for the interface that lets users design their character (with
very limited design features). This option embraces the dentist aspect of the
RPG and is very much centred around dentistry. A change was made to the input
of character traits as well - here I am trialling a choice between good, meh,
and bad for each trait.
'''

import random
from math import ceil
from time import sleep


def get_stat(prompt):
    """
    Asks user for a character stat and returns the answer.

    A character stat (e.g. self discipline, agility) is entered as either
    """
    answer = ""
    while answer not in VALID_STATS:
        answer = input(prompt).strip().lower()
        if answer not in VALID_STATS:
            print("Please select one of the three available options.")
    return answer


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
    message = list(message)
    for character in message:
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
        prompt = "How good is your self discipline (good/bad/meh)? "
        self.sd = get_stat(prompt)
        prompt = "How good is your agility (good/bad/meh)? "
        self.agility = get_stat(prompt)
        prompt = "Lastly, how healthy are your teeth (good/bad/meh)? "
        self.teeth_str = get_stat(prompt)

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

        print_slow("""
Thank you. To gain entry you must first overcome a series of tests. Good luck!
""", '')
        sleep(1)
        print_slow("""
Almost there! You turn away and head off to take the tests...""")

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

# List of three options users can choose from when choosing character traits
VALID_STATS = ("good", "bad", "meh")

if __name__ == "__main__":
    # Print prelude to character creation, then create the character
    print("Dental Hygiene RPG".center(80))
    print_slow("""
For as long you can remember you have always been devoted to a single purpose - 
the promotion of good dental hygiene. """, '')
    sleep(1)
    print_slow("As far as you are concerned, nothing else matters more. ", '')
    sleep(1)
    print_slow("That's why you're here, after all.")
    sleep(1)
    print_slow("""
The mist stirs ahead of you... and suddenly you can see it - """, '')
    sleep(1)
    print_slow("the famed guild of dentistry! ", '')
    sleep(1)
    print_slow("Your heartrate increases and you knock on the door...")
    sleep(1)
    print("\n")
    user = Player()
    # Determine relative attack damage (True - low, False - high, None - usual)
    attack_effectiveness, attacks = {}, list(SPECIFIC_MOB_ATTACKS.keys())
    for attack in range(7):
        attack_effectiveness[attacks[attack]] = user.effects[attack]
