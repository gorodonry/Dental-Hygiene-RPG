##
# opponent.py
# Date: 09/09/2021
# Author: Ryan Gordon
# Contains the opponent class for the dental RPG

import random
from math import ceil
from print_options import print_slow
from constants import STAGES, OPPONENTS, SPECIFIC_MOB_ATTACKS, WEAKNESSES, \
     STRENGTHS


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
        self.max_health = random.randint(base_health - 5, base_health + 5)
        # The more battles the user fights, the higher the health, also random
        self.max_health += ceil(random.randint(stage - 1, stage + 2) * 1.5)

        self.health = self.max_health

        # Determine available attacks, strengths, and weaknesses
        self.attacks = []
        for attack in SPECIFIC_MOB_ATTACKS:
            if self.name in SPECIFIC_MOB_ATTACKS[attack]:
                self.attacks.append(attack)

        self.weaknesses = []
        for attack in WEAKNESSES:
            if self.name in WEAKNESSES[attack]:
                self.weaknesses.append(attack)

        self.strengths = []
        for attack in STRENGTHS:
            if self.name in STRENGTHS[attack]:
                self.strengths.append(attack)

        self.extra_damage = 0
        self.damage_adjust = 1
        self.defence = OPPONENTS[self.name][2]

        self.level = OPPONENTS[self.name][1]

        # Print encounter message
        print_slow("You have encountered: ", '')
        print_slow(self.name + "!")

    def add_attack(self, attack):
        """Adds a new attack to the opponent's arsenal."""
        self.attacks.append(attack)

    def increase_attack_damage(self, amount):
        """Increases attack damage by specified amount."""
        self.extra_damage += amount

    def evolve(self):
        """
        Evolves the opponent.

        Evolve refers to either adding a new attack (default), or increasing
        attack damage slightly if arsenal is full.

        return (str/bool): False if arsenal was full before evolution, else the
            newly added attack.
        """
        if len(self.attacks) == len(SPECIFIC_MOB_ATTACKS.keys()):
            self.increase_attack_damage(1)
            return False
        else:
            available = list(SPECIFIC_MOB_ATTACKS.keys())
            for attack in self.attacks:
                available.remove(attack)
            attack = random.choice(available)
            # Ensure the chosen attack isn't a boss specific attack
            while len(SPECIFIC_MOB_ATTACKS[attack]) == 0:
                attack = random.choice(available)
            self.add_attack(attack)
            return attack

    def get_attack(self):
        """Chooses a random attack and returns it."""
        return random.choice(self.attacks)

    def adjust_damage(self, amount):
        """Adjust opponent damage by specified factor."""
        self.damage_adjust += amount

    def reset_damage_adjust(self):
        """Resets opponent damage to normal."""
        self.damage_adjust = 1

    def get_status(self):
        """Returns True if alive, False is dead."""
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
        """Restores opponent to max health."""
        self.health = self.max_health

    def increase_max_health(self, amount):
        """Increases max health by specified amount."""
        self.max_health += amount

    def increase_defence(self, amount):
        """Increases defence by specified amount."""
        self.defence += amount
