##
# battle_sequence_option_1.py
# Date: 08/09/2021
# Author: Ryan Gordon
# Option 1 of dental RPG for the battle sequence

'''
Battle sequence option 1

Option 1 for the battle sequence. This option lets the user input the attack as
a letter (with the option of typing out the entire attack), and prints out
dental hygiene messages as the battle progresses.
'''

import random
from math import ceil
from time import sleep

'''
List of classes and functions
> get_stat
> get_effect
> print_slow
> Opponent
    > __init__
    > add_attack
    > get_attack
    > get_status
    > take_damage
> Player
    > __init__
    > add_attack
    > get_attack
    > get_status
    > take_damage
    > heal
    > heal_full
    > increase_max_health
> print_prelude
> battle
'''


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
    elif stat == "good" and False in available:
        return False
    elif stat == "bad" and True in available:
        return True
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
        for attack in SPECIFIC_MOB_ATTACKS:
            if self.name in SPECIFIC_MOB_ATTACKS[attack]:
                self.attacks.append(attack)

        # Print encounter message
        print_slow("You have encountered: ", '')
        sleep(1)
        print_slow(self.name + "!")

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

    def get_attack(self):
        """Asks user to choose an attack and returns the answer."""
        # Print out options
        print("Your attacks:")
        options = {}
        for attack in self.attacks:
            option = ALPHABET[self.attacks.index(attack)]
            print(f"{attack} - {option.upper()}")
            options[option] = attack
        attack = ""
        while attack not in list(options.keys()) + list(options.values()):
            attack = input("How are you going to tackle your opponent? ")
            attack = attack.strip().lower()
            if attack not in list(options.keys()) + list(options.values()):
                print("Unfortunately, that isn't an option.")
        if attack in options.keys():
            attack = options[attack]
        return attack

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


def battle(stage):
    """
    Plays out a battle between the user and a random computer opponent.

    param stage (int): determines the possible level of the opponents.
    """
    enemy = Opponent(stage)
    turn = random.choice(["user", "computer"])
    # Loop until one or the other of the combatants is defeated
    while enemy.get_status() and user.get_status():
        print_slow(f"""
Enemy health: {enemy.health}
Your health: {user.health}""", '\n\n')
        if turn == "user":
            # User turn
            print_slow("Your turn...", '\n\n')
            sleep(1)
            attack = user.get_attack()
            sleep(1)
            # Determine relative effectiveness and with it damage
            print_slow(ATTACK_MESSAGES[attack])
            sleep(1)
            if enemy.name in WEAKNESSES[attack]:
                # If the attack is effective against the enemy
                base_damage = ceil(BASE_DAMAGE * 1.5)
                damage = random.randint(base_damage - 1, base_damage + 4)
                print_slow("""
It's super effective [""" + str(damage) + " damage]!")
            elif enemy.name in STRENGTHS[attack]:
                # If the attack is weak against the enemy
                base_damage = ceil(BASE_DAMAGE / 1.5)
                damage = random.randint(base_damage - 4, base_damage + 1)
                print_slow("""
It isn't very effective [""" + str(damage) + " damage]!")
            else:
                # If the enemy is neutral to the attack
                damage = random.randint(BASE_DAMAGE - 2, BASE_DAMAGE + 2)
                print_slow("""
The enemy manages to shake it off [""" + str(damage) + " damage].")
            enemy.take_damage(damage)
        else:
            # Opponent turn
            print_slow(enemy.name + "'s turn...")
            sleep(1)
            print()
            attack = enemy.get_attack()
            print_slow(enemy.name + " uses ", '')
            sleep(1)
            print_slow(attack + ".")
            sleep(1)
            print_slow(ATTACK_MESSAGES[attack])
            sleep(1)
            # Determine relative effectiveness and with it damage
            effect = user.affected_by[attack]
            if effect is None:
                # If user is neutral to the attack
                damage = random.randint(BASE_DAMAGE - 2, BASE_DAMAGE + 2)
                print_slow("""
You manage to shake it off [""" + str(damage) + " damage].")
            elif effect is True:
                # If the attack is effective against the user
                base_damage = ceil(BASE_DAMAGE * 1.5)
                damage = random.randint(base_damage - 1, base_damage + 4)
                print_slow("""
It's super effective [""" + str(damage) + " damage]!")
            else:
                # If the attack is weak against the user
                base_damage = ceil(BASE_DAMAGE / 1.5)
                damage = random.randint(base_damage - 4, base_damage + 1)
                print_slow("""
It isn't very effective [""" + str(damage) + " damage]!")
            user.take_damage(damage)
            sleep(1)
        # Alternate the attacks
        turn = "user" if turn == "computer" else "computer"

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
A staple in dentisrty.""",
                   "drill": """
You give your opponent a quick filling. Hopefully that hole should stop growing
now.""",
                   "fluoridated water": """
Much better than whatever they've been drinking... and fortified with fluoride!
You kind of can't go wrong.""",
                   "dental pamphlet": """
The best thing for them is to visit a dentist."""}

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
NULL_NAMES = ("Nada", "Nothing", "Null", "Zilch", "Naught")

# List of three options users can choose from when choosing character traits
VALID_STATS = ("good", "bad", "meh")

# Used for some user inputs/menus
ALPHABET = tuple("abcdefghijklmnopqrstuvwxyz")

if __name__ == "__main__":
    # Print prelude to character creation, then create the character
    print_prelude()
    user = Player()
