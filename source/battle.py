##
# battle.py
# Date: 09/09/2021
# Author: Ryan Gordon
# Contains functions used to play out a battle for the dental hygiene RPG

import random
from math import ceil
from time import sleep
from opponent import Opponent
from boss import Boss
from print_options import print_slow, print_red
from constants import STRENGTHS, BATTLE_END_MESSAGES, BASE_DAMAGE as BASE, \
     WEAKNESSES, ATTACK_MESSAGES, RANDOM_EVENTS


def battle(plr, lvl=None, strt=None, msg=None, end=None, nam=False, bos=False):
    """
    Plays out a battle between the user and a computer opponent.

    param plr (object): contains all information about the user.
    param lvl (int): determines the possible level of the opponents. Needs to
        be specified for a non-boss opponent.
    param strt (str): default is None, if set determines who strikes first.
    param msg (list): message printed before the battle starts.
    param end (list): message printed after the battle if the user wins.
    param nam (bool): returns the name of the enemy if set to True.
    param bos (str): if set, fight a boss with the specified name.

    return name (str): name of the defeated enemy (only if requested).
    """
    # Variables used in random events are declared global
    global user, enemy, turn
    # Set up user, enemy and print starting message if applicable
    user = plr
    if not bos:
        enemy, random_events = Opponent(lvl), RANDOM_EVENTS
    else:
        enemy = Boss(bos)
        random_events = RANDOM_EVENTS + enemy.start_events
    if strt is None:
        turn = random.choice(["user", "computer"])
    else:
        turn = strt
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
            random.choice(random_events)(user, enemy, turn)
            print("---------")
        print(f"\nEnemy health: {enemy.health}")
        # Print user health in red if it's low
        if user.health < 10 or (user.health < 15 and bos):
            print_red(f"Your health: {user.health}\n")
        else:
            print(f"Your health: {user.health}\n")
        if turn == "user":
            # User turn
            print_slow("Your turn...", '\n\n')
            attack = user.get_attack(enemy.name)
            print_slow(ATTACK_MESSAGES[attack])
            # Determine relative effectiveness and with it damage
            if attack in enemy.weaknesses:
                # If the attack is effective against the enemy
                base = ceil(BASE * 1.5) + user.extra_damage
                damage = random.randint(base - 1, base + 4)
                damage = ceil(damage / user.damage_adjust) - enemy.defence
                damage = 0 if damage < 0 else damage
                # 10% chance for critical if sensible attack
                critical = random.randint(0, 100) > 90
                if damage == 0:
                    print_slow("\nMissed!")
                elif critical:
                    damage *= 2
                    print_slow(f"""
CRITICAL [{damage} damage]!""")
                else:
                    print_slow(f"""
It's super effective [{damage} damage]!""")
            elif attack in enemy.strengths:
                # If the attack is weak against the enemy
                base = ceil(BASE / 1.5) + user.extra_damage
                damage = random.randint(base - 4, base + 1)
                damage = ceil(damage / user.damage_adjust) - enemy.defence
                damage = 0 if damage < 0 else damage
                if damage == 0:
                    print_slow("\nMissed!")
                else:
                    print_slow(f"""
It isn't very effective [{damage} damage]... maybe not the right attack..?""")
            else:
                # If the enemy is neutral to the attack
                base = BASE + user.extra_damage
                damage = random.randint(base - 2, base + 2)
                damage = ceil(damage / user.damage_adjust) - enemy.defence
                damage = 0 if damage < 0 else damage
                if damage == 0:
                    print_slow("\nMissed!")
                else:
                    print_slow(f"""
The {enemy.name} manages to shake it off [{damage} damage]. Hmmm...""")
            enemy.take_damage(damage)
            # Reset temporary effects from random events
            user.uncompromise_all_attacks()
            user.reset_damage_adjust()
            # Add any boss specific random events that have to occur later
            if bos:
                # The set avoids duplicates
                random_events = set(random_events)
                random_events.update(enemy.later_events)
                random_events = list(random_events)
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
                if damage == 0:
                    print_slow("\nMissed!")
                else:
                    print_slow(f"""
You manage to shake it off [{damage} damage].""")
            elif effect is True:
                # If the attack is effective against the user
                base = ceil(BASE * 1.5) + enemy.extra_damage
                damage = random.randint(base - 1, base + 4)
                damage = ceil(damage / enemy.damage_adjust) - user.defence
                damage = 0 if damage < 0 else damage
                if damage == 0:
                    print_slow("\nMissed!")
                else:
                    print_slow(f"""
It's super effective [{damage} damage]! Ouch ouch ouch...""")
            else:
                # If the attack is weak against the user
                base = ceil(BASE / 1.5) + enemy.extra_damage
                damage = random.randint(base - 4, base + 1)
                damage = ceil(damage / enemy.damage_adjust) - user.defence
                damage = 0 if damage < 0 else damage
                if damage == 0:
                    print_slow("\nMissed!")
                else:
                    print_slow(f"""
It isn't very effective [{damage} damage]. Take that, {enemy.name}!""")
            user.take_damage(damage)
            # Reset temporary effects from random events
            enemy.reset_damage_adjust()
        # Alternate the attacks and check for random event next round
        turn = "user" if turn == "computer" else "computer"
        if not bos:
            random_event = random.randint(0, 100) > 60
        else:
            random_event = random.randint(0, 100) > 40
    # Print success/death message
    print()
    if user.get_status():
        print_slow("Victory!")
        if not bos:
            print_slow(BATTLE_END_MESSAGES[enemy.name])
        else:
            print()
            enemy.death_message()
        if end is not None:
            print()
            for line in end:
                print_slow(line[0], line[1])
        user.heal_full()
        print_slow("""
Following the battle you spend a couple of minutes with an electric toothbrush,
thoroughly cleaning your teeth (restoration to max health).""")
    else:
        print_slow("You died...")
    if nam:
        return enemy.name
