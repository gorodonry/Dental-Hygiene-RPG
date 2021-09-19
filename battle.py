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
from constants import STRENGTHS, BATTLE_END_MESSAGES, BASE_DAMAGE as BASE, \
     WEAKNESSES, ATTACK_MESSAGES


def evolve_monster():
    """Adds an attack to the monsters arsenal and prints context."""
    attack = enemy.evolve()
    print_slow(f"Something's happening to the {enemy.name}... ", '')
    sleep(1)
    print_slow("it appears to be evolving!")
    sleep(1)
    print()
    if attack:
        print_slow(f"It's developed another attack: {attack}...")
    else:
        print_slow("The incoming attack looks deadlier to your trained eye...")
    sleep(3)


def compromise_attack():
    """Compromises a users attack and prints context."""
    attack = user.compromise()
    print_slow(f"Plaque have taken down your {attack}!")
    sleep(1)
    print()
    print_slow("You quickly cleanse it - should be working again next time...")
    sleep(3)


def find_toothbrush():
    """Heals user slightly and prints context."""
    amount = user.heal(random.randint(5, 8))
    print_slow("There's something in your pocket... ", '')
    sleep(1)
    print_slow("it's a manual toothbrush!")
    sleep(1)
    if amount is not None:
        print_slow(f"\nYou give your teeth a quick clean (healed {amount}hp).")
    else:
        user.increase_attack_damage(1)
        print_slow("""
You're feeling stronger than ever after giving your teeth a quick clean (attack
damage increased by 1).""")
    sleep(3)


def gust():
    """Reduce damage for the next attack by half."""
    if turn == "user":
        user.adjust_damage(1)
        print_slow("A gust of wind buffets you around!")
        sleep(1)
        print_slow("\nDamage of your next attack reduced by half...")
    else:
        enemy.adjust_damage(1)
        print_slow(f"A gust of wind buffets the {enemy.name} around!")
        sleep(1)
        print_slow("\nDamage of their next attack reduced by half...")
    sleep(3)


def battle(stage, player, start=None):
    """
    Plays out a battle between the user and a random computer opponent.

    param stage (int): determines the possible level of the opponents.
    param player (object): contains all information about the user.
    param start (str): default is None, if set determines who strikes first.

    return user (object): all information about the user following the battle.
    """
    # Variables used in random events are declared global
    global user, enemy, turn
    user, enemy = player, Opponent(stage)
    if start is None:
        turn = random.choice(["user", "computer"])
    else:
        turn = start
    random_event = False
    # Loop until one or the other of the combatants is defeated
    while enemy.get_status() and user.get_status():
        # If a random event takes place, print the event and apply its effect
        if random_event:
            print_slow("\n--EVENT--")
            sleep(1)
            random.choice(RANDOM_EVENTS)()
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
                base = ceil(BASE * 1.5) + user.extra_damage
                damage = random.randint(base - 1, base + 4)
                damage = ceil(damage / user.damage_adjust)
                # 10% chance for critical if sensible attack
                critical = random.randint(0, 100) > 90
                if critical:
                    damage *= 2
                    print_slow(f"""
CRITICAL [{damage} damage]!""")
                else:
                    print_slow(f"""
It's super effective [{damage} damage]!""")
            elif enemy.name in STRENGTHS[attack]:
                # If the attack is weak against the enemy
                base = ceil(BASE / 1.5) + user.extra_damage
                damage = random.randint(base - 4, base + 1)
                damage = ceil(damage / user.damage_adjust)
                print_slow(f"""
It isn't very effective [{damage} damage]... maybe not the right attack..?""")
            else:
                # If the enemy is neutral to the attack
                base = BASE + user.extra_damage
                damage = random.randint(base - 2, base + 2)
                damage = ceil(damage / user.damage_adjust)
                print_slow(f"""
The {enemy.name} manages to shake it off [{damage} damage]. Hmmm...""")
            enemy.take_damage(damage)
            sleep(1)
            # Reset temporary effects from random events
            user.uncompromise_all_attacks()
            user.reset_damage_adjust()
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
                base = BASE + enemy.extra_damage
                damage = random.randint(base - 2, base + 2)
                damage = ceil(damage / enemy.damage_adjust)
                print_slow(f"""
You manage to shake it off [{damage} damage].""")
            elif effect is True:
                # If the attack is effective against the user
                base = ceil(BASE * 1.5) + enemy.extra_damage
                damage = random.randint(base - 1, base + 4)
                damage = ceil(damage / enemy.damage_adjust)
                print_slow(f"""
It's super effective [{damage} damage]! Ouch ouch ouch...""")
            else:
                # If the attack is weak against the user
                base = ceil(BASE / 1.5) + enemy.extra_damage
                damage = random.randint(base - 4, base + 1)
                damage = ceil(damage / enemy.damage_adjust)
                print_slow(f"""
It isn't very effective [{damage} damage]. Take that, {enemy.name}!""")
            user.take_damage(damage)
            sleep(1)
            # Reset temporary effects from random events
            enemy.reset_damage_adjust()
        # Alternate the attacks and check for random event next round
        turn = "user" if turn == "computer" else "computer"
        random_event = random.randint(0, 100) > 60
    # Print success/death message
    print()
    if user.get_status():
        print_slow("Victory!")
        sleep(1)
        print_slow(BATTLE_END_MESSAGES[enemy.name])
    else:
        print_slow("You died...")
    return user

RANDOM_EVENTS = (evolve_monster, compromise_attack, find_toothbrush, gust)
