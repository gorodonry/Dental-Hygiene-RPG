##
# battle_sequence_option_3.py
# Date: 09/09/2021
# Author: Ryan Gordon
# Option 3 of dental RPG for the battle sequence

'''
Battle sequence option 2

*description
'''

import random
from math import ceil
from time import sleep
from opponent import Opponent
from player import Player
from print_options import print_slow
from constants import WEAKNESSES, BASE_DAMAGE, STRENGTHS, ATTACK_MESSAGES, \
     BATTLE_END_MESSAGES


def print_prelude():
    """Prints the prelude to the game."""
    print("Dental Hygiene RPG".center(80))
    print_slow("""
You walk up the empty street and turn left. """, '')
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
    print_slow("the famed door!")
    sleep(1)
    print()
    print_slow("Your heartrate increases as you knock on it...")
    sleep(1)
    print("\n")


def battle(stage, user, start=None):
    """
    Plays out a battle between the user and a random computer opponent.

    param stage (int): determines the possible level of the opponents.
    """
    enemy = Opponent(stage)
    turn = random.choice(["user", "computer"]) if start is None else start
    # Loop until one or the other of the combatants is defeated
    while enemy.get_status() and user.get_status():
        print_slow(f"""
Remaining enemy hits: {enemy.health}
Your remaining hits: {user.health}""", '\n\n')
        if turn == "user":
            # User turn
            print_slow("Your turn...", '\n\n')
            sleep(1)
            attack = user.get_attack(3)
            sleep(1)
            # Determine relative effectiveness and with it damage
            print()
            print_slow(f"You chose {attack}.")
            sleep(1)
            print_slow(ATTACK_MESSAGES[attack])
            sleep(1)
            if enemy.name in WEAKNESSES[attack]:
                # If the attack is effective against the enemy
                base_damage = ceil(BASE_DAMAGE * 1.5)
                damage = random.randint(base_damage - 1, base_damage + 4)
                print_slow(f"""
It does a lot of damage ({damage})!""")
            elif enemy.name in STRENGTHS[attack]:
                # If the attack is weak against the enemy
                base_damage = ceil(BASE_DAMAGE / 1.5)
                damage = random.randint(base_damage - 4, base_damage + 1)
                print_slow(f"""
The {enemy.name} hardly notices your attack... maybe not the right one..?""")
            else:
                # If the enemy is neutral to the attack
                damage = random.randint(BASE_DAMAGE - 2, BASE_DAMAGE + 2)
                print_slow(f"""
It does a bit of damage ({damage}).""")
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
                print_slow(f"""
It's just a flesh wound ({damage}).""")
            elif effect is True:
                # If the attack is effective against the user
                base_damage = ceil(BASE_DAMAGE * 1.5)
                damage = random.randint(base_damage - 1, base_damage + 4)
                print_slow(f"""
Youch! {damage} hits...""")
            else:
                # If the attack is weak against the user
                base_damage = ceil(BASE_DAMAGE / 1.5)
                damage = random.randint(base_damage - 4, base_damage + 1)
                print_slow("""
Did they just attack? All that for no effect...""")
            user.take_damage(damage)
            sleep(1)
        # Alternate the attacks
        turn = "user" if turn == "computer" else "computer"
    print()
    if user.get_status():
        print_slow("Victory!")
        sleep(1)
        print_slow(BATTLE_END_MESSAGES[enemy.name])
    else:
        print_slow("Oof. You died...")
    return user

if __name__ == "__main__":
    # Print the prelude before creating a character
    #print_prelude()
    user = Player()
    print("\n")
    # Fight a battle against a level 1 monster with no context
    user = battle(1, user, "user")
