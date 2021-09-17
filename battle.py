##
# battle.py
# Date: 09/09/2021
# Author: Ryan Gordon
# Contains functions used to play out a battle for the dental hygiene RPG

import random
from math import ceil
from time import sleep
from opponent import Opponent
from print_options import print_slow
from constants import ATTACK_MESSAGES, WEAKNESSES, STRENGTHS, BASE_DAMAGE, \
     BATTLE_END_MESSAGES


def battle(stage, user, start=None):
    """
    Plays out a battle between the user and a random computer opponent.

    param stage (int): determines the possible level of the opponents.
    param user (object): contains all information about the user.
    param start (str): default is None, if set determines who strikes first.
    """
    enemy = Opponent(stage)
    if start is None:
        turn = random.choice(["user", "computer"])
    else:
        turn = start
    # Loop until one or the other of the combatants is defeated
    while enemy.get_status() and user.get_status():
        print_slow(f"""
Enemy health: {enemy.health}
Your health: {user.health}""", '\n\n')
        if turn == "user":
            # User turn
            print_slow("Your turn...", '\n\n')
            sleep(1)
            attack = user.get_attack(enemy.name)
            sleep(1)
            # Determine relative effectiveness and with it damage
            print_slow(ATTACK_MESSAGES[attack])
            sleep(1)
            if enemy.name in WEAKNESSES[attack]:
                # If the attack is effective against the enemy
                base_damage = ceil(BASE_DAMAGE * 1.5)
                damage = random.randint(base_damage - 1, base_damage + 4)
                print_slow(f"""
It's super effective [{damage} damage]!""")
            elif enemy.name in STRENGTHS[attack]:
                # If the attack is weak against the enemy
                base_damage = ceil(BASE_DAMAGE / 1.5)
                damage = random.randint(base_damage - 4, base_damage + 1)
                print_slow(f"""
It isn't very effective [{damage} damage]... maybe not the right attack..?""")
            else:
                # If the enemy is neutral to the attack
                damage = random.randint(BASE_DAMAGE - 2, BASE_DAMAGE + 2)
                print_slow(f"""
The {enemy.name} manages to shake it off [{damage} damage]. Hmmm...""")
            enemy.take_damage(damage)
            sleep(1)
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
                print_slow(f"""
You manage to shake it off [{damage} damage].""")
            elif effect is True:
                # If the attack is effective against the user
                base_damage = ceil(BASE_DAMAGE * 1.5)
                damage = random.randint(base_damage - 1, base_damage + 4)
                print_slow(f"""
It's super effective [{damage} damage]! Ouch ouch ouch...""")
            else:
                # If the attack is weak against the user
                base_damage = ceil(BASE_DAMAGE / 1.5)
                damage = random.randint(base_damage - 4, base_damage + 1)
                print_slow(f"""
It isn't very effective [{damage} damage]. Take that, {enemy.name}!""")
            user.take_damage(damage)
            sleep(1)
        # Alternate the attacks
        turn = "user" if turn == "computer" else "computer"
    # Print success/death message
    print()
    if user.get_status():
        print_slow("Victory!")
        sleep(1)
        print_slow(BATTLE_END_MESSAGES[enemy.name])
    else:
        print_slow("You died...")
    return user
