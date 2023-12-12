##
# battle_functions.py
# Date: 23/09/2021
# Author: Ryan Gordon
# Contains functions used during the battle sequence

import random
from time import sleep
from print_options import print_slow


def evolve_monster(user, enemy, turn):
    """
    Adds an attack to the monsters arsenal and prints context.

    Random event.
    """
    attack = enemy.evolve()
    print_slow(f"Something's happening to the {enemy.name}... ", '')
    print_slow("it appears to be evolving!")
    print()
    if attack:
        print_slow(f"It's developed another attack: {attack}...")
    else:
        print_slow("The incoming attack looks deadlier to your trained eye...")
    sleep(2)


def compromise_attack(user, enemy, turn):
    """
    Compromises a users attack and prints context.

    Random event.
    """
    attack = user.compromise()
    print_slow(f"Plaque have taken down your {attack}!")
    print()
    print_slow("You quickly cleanse it - should be working again next time...")
    sleep(2)


def find_toothbrush(user, enemy, turn):
    """
    Heals user slightly and prints context.

    Random event.
    """
    amount = user.heal(random.randint(5, 8))
    print_slow("There's something in your pocket... ", '')
    print_slow("it's a manual toothbrush!")
    if amount is not None:
        print_slow(f"\nYou give your teeth a quick clean (healed {amount}hp).")
    else:
        user.increase_attack_damage(1)
        print_slow("""
You're feeling stronger than ever after giving your teeth a quick clean (attack
damage increased by 1).""")
    sleep(2)


def gust(user, enemy, turn):
    """
    Reduce damage for the next attack by half.

    Random event.
    """
    if turn == "user":
        user.adjust_damage(1)
        print_slow("A gust of wind buffets you around!")
        print_slow("\nDamage of your next attack reduced by half...")
    else:
        enemy.adjust_damage(1)
        print_slow(f"A gust of wind buffets the {enemy.name} around!")
        print_slow("\nDamage of their next attack reduced by half...")
    sleep(2)


def coke_start():
    """Message printed when encountering the coke boss."""
    print_slow("'You think you can stop this?")
    print_slow("""
'You will be crushed underfoot like any other who stands in my way. It's one of
the fundamental rules of existence. """, '', wait=0.015)
    print_slow("I always win.'", gap=0.2)
    print_slow("\n'Time someone changed them then.'")


def coke_end():
    """Message printed after defeating the coke boss."""
    print_slow("'Not possible...", gap=0.2)
    print_slow("\n'You're all so addicted to sugar... ", '')
    print_slow("it should've been easy...")
    print_slow("\n'I...' *blerrr*")


def fizz(user, enemy, turn):
    """
    Permanently decreases user attack damage by 1.

    Coke boss specific random event.
    """
    print_slow("A pressure build-up has caused coke to spray everywhere!")
    decreased = user.decrease_attack_damage(1)
    if decreased:
        print_slow("""
You can feel it affecting you... (attack damage decreased by 1).""")
    else:
        print_slow("""
Your movements become sluggish while confronted by all the coke (damage of your
next attack reduced by half).""")
    sleep(2)


def pressure_release(user, enemy, turn):
    """
    Permanently decreases coke attack damage by 1.

    Coke boss specific random event.
    """
    print_slow("Your last attack was even more successful than you thought!")
    decreased = enemy.decrease_attack_damage(1)
    if decreased:
        print_slow("""
It released some pressure from the bottle (enemy damage decreased by 1).""")
    else:
        print_slow("\nYou stunned your opponent! ", '')
        print_slow("Damage of their next attack significantly reduced!")
    sleep(2)


def dissolve_weapon(user, enemy, turn):
    """
    Permanently removes one of the users weapons (determined randomly).

    Coke boss specific random event.
    """
    print_slow("The coke has gotten onto your weapons...")
    weapon = user.delete_attack()
    if weapon:
        print_slow(f"\nIt's dissolved your {weapon}!")
    else:
        print_slow(f"""
Nooo! Not your {user.attacks[0]} too! You frantically wipe it down...""")
    sleep(2)
