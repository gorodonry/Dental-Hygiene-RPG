##
# player.py
# Date: 09/09/2021
# Author: Ryan Gordon
# Contains the player class for the dental RPG and relevant functions

import random
from math import ceil
from time import sleep
from print_options import print_slow
from constants import VALID_STATS, NULL_NAMES, AVAILABLE_EFFECTS, OPPONENTS, \
     SPECIFIC_MOB_ATTACKS, WEAKNESSES, ALPHABET


def get_stat(prompt, stats):
    """
    Asks user for a character stat and returns the answer.

    A character stat (e.g. self discipline, agility) is entered as either good,
    bad, or meh.
    """
    ans, valid_stats = "", list(VALID_STATS.values())
    while ans not in valid_stats or (stats.count(ans) == 2 and ans != "meh"):
        ans = input(prompt).strip().lower()
        if ans not in valid_stats:
            try:
                ans = VALID_STATS[ans]
            except KeyError:
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

    def get_attack(self, option=None):
        """Asks user to choose an attack and returns the answer."""
        # Interface used in the final product
        if option is None:
            'placeholder'
        # Interface for battle sequence option 1
        elif option == 1:
            # Print out options
            print("Your attacks:")
            options = {}
            for attack in self.attacks:
                option = ALPHABET[self.attacks.index(attack)]
                print(f"{attack} - {option.upper()}")
                options[option] = attack
            attack = ""
            # Determine the attack
            while attack not in list(options.keys()) + list(options.values()):
                attack = input("How are you going to tackle your opponent? ")
                attack = attack.strip().lower()
                if attack not in list(options.keys()) + list(options.values()):
                    print("Unfortunately, that isn't an option.")
            if attack in options.keys():
                attack = options[attack]
        # Interface for battle sequence option 2
        elif option == 2:
            # Print out options
            print("Available weapons:")
            for attack in self.attacks:
                option = self.attacks.index(attack)
                print(f"({option + 1}) {attack}")
            attack = ""
            # Determine the attack
            while attack not in self.attacks:
                attack = input("Choose your weapon: ").strip().lower()
                if attack not in self.attacks:
                    try:
                        attack = self.attacks[int(attack) - 1]
                    except ValueError:
                        print("Not currently in your arsenal.")
        # Interface for battle sequence option 3
        else:
            # Print out options
            print(f"Equipment in your backpack: {', '.join(self.attacks)}.")
            attack = ""
            # Determine the attack
            while attack not in self.attacks:
                attack = input("What are you going to use? ")
                if attack not in self.attacks:
                    print("Try using something from your backpack...")
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
