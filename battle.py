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
    print_slow("it appears to be evolving!")
    print()
    if attack:
        print_slow(f"It's developed another attack: {attack}...")
    else:
        print_slow("The incoming attack looks deadlier to your trained eye...")
    sleep(2)


def compromise_attack():
    """Compromises a users attack and prints context."""
    attack = user.compromise()
    print_slow(f"Plaque have taken down your {attack}!")
    print()
    print_slow("You quickly cleanse it - should be working again next time...")
    sleep(2)


def find_toothbrush():
    """Heals user slightly and prints context."""
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


def gust():
    """Reduce damage for the next attack by half."""
    if turn == "user":
        user.adjust_damage(1)
        print_slow("A gust of wind buffets you around!")
        print_slow("\nDamage of your next attack reduced by half...")
    else:
        enemy.adjust_damage(1)
        print_slow(f"A gust of wind buffets the {enemy.name} around!")
        print_slow("\nDamage of their next attack reduced by half...")
    sleep(2)


def battle(stage, player, start=None, msg=None, end_msg=None, name=False):
    """
    Plays out a battle between the user and a random computer opponent.

    param stage (int): determines the possible level of the opponents.
    param player (object): contains all information about the user.
    param start (str): default is None, if set determines who strikes first.
    param msg (list): message printed before the battle starts.
    param end_msg (list): message printed after the battle if the user wins.
    param name (bool): returns the name of the enemy if set to True.

    return user (object)[, name (str)]: all information about the user
        following the battle[, name of the monster they just fought].
    """
    # Variables used in random events are declared global
    global user, enemy, turn
    user, enemy = player, Opponent(stage)
    if start is None:
        turn = random.choice(["user", "computer"])
    else:
        turn = start
    if msg is not None:
        print_slow(f"\nThe {enemy.name} is saying something...")
        print()
        for line in msg:
            print_slow(line[0], line[1])
        sleep(2)
    random_event = False
    # Loop until one or the other of the combatants is defeated
    while enemy.get_status() and user.get_status():
        # If a random event takes place, print the event and apply its effect
        if random_event:
            print("\n--EVENT--")
            sleep(1)
            random.choice(RANDOM_EVENTS)()
            print("---------")
        print_slow(f"""
Enemy health: {enemy.health}
Your health: {user.health}""", '\n\n')
        if turn == "user":
            # User turn
            print_slow("Your turn...", '\n\n')
            attack = user.get_attack(enemy.name)
            # Determine relative effectiveness and with it damage
            print_slow(ATTACK_MESSAGES[attack])
            if enemy.name in WEAKNESSES[attack]:
                # If the attack is effective against the enemy
                base = ceil(BASE * 1.5) + user.extra_damage
                damage = random.randint(base - 1, base + 4)
                damage = ceil(damage / user.damage_adjust)
                damage = 0 if damage < 0 else damage
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
                damage = 0 if damage < 0 else damage
                print_slow(f"""
It isn't very effective [{damage} damage]... maybe not the right attack..?""")
            else:
                # If the enemy is neutral to the attack
                base = BASE + user.extra_damage
                damage = random.randint(base - 2, base + 2)
                damage = ceil(damage / user.damage_adjust)
                damage = 0 if damage < 0 else damage
                print_slow(f"""
The {enemy.name} manages to shake it off [{damage} damage]. Hmmm...""")
            enemy.take_damage(damage)
            # Reset temporary effects from random events
            user.uncompromise_all_attacks()
            user.reset_damage_adjust()
        else:
            # Opponent turn
            print_slow(f"{enemy.name}'s turn...")
            attack = enemy.get_attack()
            print_slow(f"\n{enemy.name} uses ", '')
            print_slow(attack + ".")
            print_slow(ATTACK_MESSAGES[attack])
            # Determine relative effectiveness and with it damage
            effect = user.affected_by[attack]
            if effect is None:
                # If user is neutral to the attack
                base = BASE + enemy.extra_damage
                damage = random.randint(base - 2, base + 2)
                damage = ceil(damage / enemy.damage_adjust) - user.defence
                damage = 0 if damage < 0 else damage
                print_slow(f"""
You manage to shake it off [{damage} damage].""")
            elif effect is True:
                # If the attack is effective against the user
                base = ceil(BASE * 1.5) + enemy.extra_damage
                damage = random.randint(base - 1, base + 4)
                damage = ceil(damage / enemy.damage_adjust) - user.defence
                damage = 0 if damage < 0 else damage
                print_slow(f"""
It's super effective [{damage} damage]! Ouch ouch ouch...""")
            else:
                # If the attack is weak against the user
                base = ceil(BASE / 1.5) + enemy.extra_damage
                damage = random.randint(base - 4, base + 1)
                damage = ceil(damage / enemy.damage_adjust) - user.defence
                damage = 0 if damage < 0 else damage
                print_slow(f"""
It isn't very effective [{damage} damage]. Take that, {enemy.name}!""")
            user.take_damage(damage)
            # Reset temporary effects from random events
            enemy.reset_damage_adjust()
        # Alternate the attacks and check for random event next round
        turn = "user" if turn == "computer" else "computer"
        random_event = random.randint(0, 100) > 60
    # Print success/death message
    print()
    if user.get_status():
        print_slow("Victory!")
        print_slow(BATTLE_END_MESSAGES[enemy.name])
        if end_msg is not None:
            print()
            for line in end_msg:
                print_slow(line[0], line[1])
            sleep(2)
        user.heal_full()
        print_slow("""
Following the battle you spend a couple of minutes with an electric toothbrush,
thoroughly cleaning your teeth (restoration to max health).""")
    else:
        print_slow("You died...")
    if name:
        return enemy.name

RANDOM_EVENTS = (evolve_monster, compromise_attack, find_toothbrush, gust)
