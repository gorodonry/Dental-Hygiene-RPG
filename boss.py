##
# boss.py
# Date: 22/09/2021
# Author: Ryan Gordon
# Contains the boss class for the dental RPG and relevant functions

import random
from print_options import print_slow
from constants import BOSSES, SPECIFIC_MOB_ATTACKS


class Boss:
    """Creates a boss object."""

    def __init__(self, name=None):
        """
        Basic setup and variables for the boss.

        param name (str): if specified, determines the boss being faced,
            otherwise randomly chosen.
        """

        # Determine boss based off name parameter, or randomly if nothing there
        if name is not None:
            self.name = name
        else:
            self.name = random.choice(BOSSES.keys())

        # Determine health with a random component
        base_health = BOSSES[self.name][0]
        self.max_health = random.randint(base_health - 5, base_health + 5)
        self.health = self.max_health

        # Determine available attacks, strengths, and weaknesses
        self.attacks = list(BOSSES[self.name][3])
        self.weaknesses = BOSSES[self.name][4]
        self.strengths = BOSSES[self.name][5]

        self.events = BOSSES[self.name][7]

        self.extra_damage = 1
        self.damage_adjust = 1
        self.defence = BOSSES[self.name][2]

        self.level = BOSSES[self.name][1]

        # Print encounter message
        BOSSES[self.name][6][0]()

    def add_attack(self, attack):
        """Adds a new attack to the boss' arsenal."""
        self.attacks.append(attack)

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

    def evolve(self):
        """
        Evolves the boss.

        Evolve refers to either adding a new attack (default), or increasing
        attack damage slightly if arsenal is full.

        return (str/bool): False if arsenal was full before evolution, else the
            newly added attack.
        """
        if len(self.attacks) == len(SPECIFIC_MOB_ATTACKS.keys()):
            increased = self.increase_attack_damage(1)
            return False
        else:
            available = list(SPECIFIC_MOB_ATTACKS.keys())
            for attack in self.attacks:
                available.remove(attack)
            self.add_attack(random.choice(available))
            return self.attacks[-1]

    def get_attack(self):
        """Chooses a random attack and returns it."""
        return random.choice(self.attacks)

    def adjust_damage(self, amount):
        """Adjust boss damage by specified factor."""
        self.damage_adjust += amount

    def reset_damage_adjust(self):
        """Resets boss damage to normal."""
        self.damage_adjust = 1

    def get_status(self):
        """Returns True if alive, False if dead."""
        return self.health > 0

    def take_damage(self, damage):
        """Reduces health based on user damage."""
        self.health -= damage

    def heal(self, amount):
        """Increases health by specified amount (up to the max)."""
        if self.health + amount >= self.max_health:
            self.health = self.max_health
        else:
            self.health += amount

    def heal_full(self):
        """Restores boss to full health."""
        self.health = self.max_health

    def increase_max_health(self, amount):
        """Increases max health by specified amount."""
        self.max_health += amount

    def increase_defence(self, amount):
        """Increases defence by specified amount."""
        self.defence += amount

    def death_message(self):
        """Prints success dialogue if the user kills the boss."""
        BOSSES[self.name][6][1]()
