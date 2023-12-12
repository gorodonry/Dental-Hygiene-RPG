##
# player.py
# Date: 09/09/2021
# Author: Ryan Gordon
# Contains the player class for the dental RPG and relevant functions

import random
from math import ceil
from time import sleep
from print_options import print_slow, print_red
from constants import VALID_STATS, NULL_NAMES, AVAILABLE_EFFECTS, OPPONENTS, \
     SPECIFIC_MOB_ATTACKS, WEAKNESSES, ATTACK_HELP, BASE_DAMAGE
import sys


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
        if stats.count(ans) == 2 and ans != "meh":
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


def print_attacks(attacks, compromised):
    """Prints out available user attacks. Returns number of attacks."""
    print("Equipment in your backpack:")
    for attack in attacks:
        option = attacks.index(attack)
        # Compromised attacks are printed in red
        if attack not in compromised:
            print(f"({option + 1}) {attack}")
        else:
            print_red(f"({option + 1}) {attack}")
    # Typing help or the corresponding number gives information on attacks
    print(f"({option + 2}) help")
    return option


class Player:
    """Creates an object that contains all the player's information."""

    def __init__(self):
        """Initial setup of character."""
        # Start of character creation messages
        print_slow("Greetings applicant", '\n\n')
        print_slow("We need some information about you.", '\n\n')

        print("Guild application form\n")

        # Get player name
        self.name = input("Name: ").strip()
        if self.name == "":
            self.name = random.choice(NULL_NAMES)
            sleep(1)
            print_slow("You need a name to enter.")
            print_slow("We have decided you shall henceforth be known as ", '')
            print_slow(f"{self.name}.")

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

        self.extra_damage = 0
        self.damage_adjust = 1
        self.defence = 0

        # During a battle, attacks can stop working due to a random event
        self.compromised_attacks = []

        self.level = 1

        # Print game situation and stats of resultant character
        self.print_stats()

        print_slow("\nThank you. ", '')
        print_slow("But this is just writing. ", '')
        print_slow("Prior to joining you must undergo a series of tests.")
        print()
        print_slow("The assessor shows you another door and steps back. ", '')
        print_slow("You open it...")

    def add_attack(self, attack):
        """Adds a new attack to the player's arsenal."""
        self.attacks.append(attack)

    def get_attack(self, enemy):
        """Asks user to choose an attack and returns the answer."""
        # Print out options
        option = print_attacks(self.attacks, self.compromised_attacks)
        attack = ""
        # Determine the attack, check for validity
        while attack not in self.attacks or attack in self.compromised_attacks:
            # If they asked for help with the attacks, print the attacks again
            if attack in ("help", str(option + 2)):
                option = print_attacks(self.attacks, self.compromised_attacks)
            attack = input("How will you tackle your enemy? ").strip().lower()
            # If the user wants information on an attack or two
            if attack in ("help", str(option + 2)):
                print_slow("""
You wave the monster down. 'Just give me a minute to consult my dental handbook
please...'""")
                print("\n(Press enter to put the handbook down.)")
                attack_help = " "
                # Loop until the user hits enter, means they want to attack
                while attack_help != "":
                    # Ask for the attack to help with
                    attack_help = input("What attack do you want to look up? ")
                    attack_help = attack_help.strip().lower()
                    # If the attack was likely entered as a number, convert it
                    if attack_help not in self.attacks and attack_help != "":
                        try:
                            attack_help = int(attack_help) - 1
                            if attack_help >= 0:
                                # If the requirements are satisfied, print help
                                attack_help = self.attacks[attack_help]
                                message = ATTACK_HELP[attack_help].split("*")
                                print_slow(message[0], '')
                                print_slow(message[1], gap=0.015)
                                print()
                            else:
                                print("You seem unable to find the entry...")
                        except ValueError:
                            print(f"There's no entry for {attack_help}...")
                        except IndexError:
                            print("You seem unable to find the entry...")
                    elif attack_help != "":
                        # If the requirements are satisfied, print help
                        message = ATTACK_HELP[attack_help].split("*")
                        print_slow(message[0], '')
                        print_slow(message[1], gap=0.015)
                        print()
                    else:
                        # User is exiting the help menu
                        print_slow("""
You stow your handbook and apologise to the monster. 'Ok I'm ready now...'""")
                        print_slow(f"\nThe {enemy} glares at you.")
                        print()
            # If the attack was likely entered as a number, convert it
            elif attack not in self.attacks:
                try:
                    attack = int(attack) - 1
                    if attack >= 0:
                        attack = self.attacks[attack]
                    else:
                        print("That doesn't correspond to anything...")
                except ValueError:
                    print("Not currently in your arsenal.")
                except IndexError:
                    print("That doesn't correspond to anything...")
            if attack in self.compromised_attacks:
                print("You reach for it but it isn't working...")
        return attack

    def delete_attack(self, attack=None):
        """Deletes an existing attack from the player's arsenal."""
        if len(self.attacks) == 1:
            return False
        elif attack is None:
            attack = random.choice(self.attacks)
            self.attacks.remove(attack)
            return attack
        else:
            self.attacks.remove(attack)

    def compromise(self, attack=None):
        """Adds an attack to the compromised attacks list."""
        # Compromise either a specified or a random attack
        if attack is None:
            self.compromised_attacks.append(random.choice(self.attacks))
        else:
            self.compromised_attacks.append(attack)
        return self.compromised_attacks[-1]

    def uncompromise_all_attacks(self):
        """Uncompromises all player attacks."""
        self.compromised_attacks = []

    def adjust_damage(self, amount):
        """Adjust user damage by specified factor."""
        self.damage_adjust += amount

    def reset_damage_adjust(self):
        """Resets user damage to normal."""
        self.damage_adjust = 1

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
            return None
        else:
            self.health += amount
            return amount

    def heal_full(self):
        """Restores user to max health."""
        self.health = self.max_health

    def increase_max_health(self, amount):
        """Increases max health by specified amount."""
        self.max_health += amount

    def increase_attack_damage(self, amount):
        """Increases attack damage by specified amount."""
        self.extra_damage += amount

    def decrease_attack_damage(self, amount):
        """Decreases attack damage by specified amount."""
        if self.extra_damage - amount < 0:
            self.adjust_damage(1)
            return False
        else:
            self.extra_damage -= amount
            return True

    def increase_defence(self, amount):
        """Increases defence by specified amount."""
        self.defence += amount

    def print_stats(self, level_up=False):
        """Prints out all user stats in a nice fashion."""
        if not level_up:
            print_slow("\n--Your character--")
        else:
            print_slow("Your enhanced stats")
        print_slow(f"{self.name} (level {self.level})")
        print_slow(f"""
Attack damage: {BASE_DAMAGE + self.extra_damage}""", wait=0.015)
        print_slow(f"Defence: {self.defence}", wait=0.015)
        print_slow(f"Max health: {self.max_health}")
        strong_against, weak_against = [], []
        for attack in self.affected_by:
            if self.affected_by[attack] is False:
                strong_against.append(attack)
            elif self.affected_by[attack] is True:
                weak_against.append(attack)
        print_slow(f"""
Strong against: {', '.join(strong_against)}""", wait=0.015)
        print_slow(f"Weak against: {', '.join(weak_against)}")
        print(f"------------{'------' if not level_up else ''}")

    def level_up(self):
        """Levels the user up and gives stats a subsequent boost."""
        print("\n--LEVEL UP--")
        self.level += 1
        print_slow(f"You've reached level {self.level}!")
        self.increase_max_health(15)
        self.heal_full()
        self.increase_attack_damage(2)
        print_slow("Increased attack damage (by 2) and health (by 15).")
        print()
        self.print_stats(True)
