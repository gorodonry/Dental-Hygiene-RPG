##
# main.py
# Date: 08/09/2021
# Author: Ryan Gordon
# Plays as PRG game with the user as a dentist, promotes good dental hygiene

import random
from time import sleep
from battle import battle
from player import Player
from print_options import print_slow
from constants import FOREST_ENCOUNTER_MESSAGE as FOREST_MOB_MSG, \
     TOWER_ENCOUNTER_MESSAGE as TWR_MB_MSG, FOREST_OUTSKIRTS_ENCOUNTER, \
     FOREST_ROUTES


def next_part(part, msg=''):
    """Prints a break in the story telling to signal a new 'chapter'."""
    print("\n-----")
    print_slow(f"End of part {part}.")
    to_print = f"\nPart {part + 1}{':' if msg != '' else ''} {msg} loading"
    print_slow(to_print, '', wait=0.5)
    print_slow(".....", gap=0.5, wait=0)
    print("-----\n")


def prologue():
    """Prints the prologue to the game."""
    print("Dental Hygiene RPG".center(80))
    print_slow("\nYou walk up the empty street and turn left. ", '')
    print_slow("Another dark alleyway.")
    print_slow("\nThe kingdom hasn't been the same lately; ", '')
    print_slow("""rumours of a great evil roaming across
the land have been circulating. """, '')
    print_slow("Rumours that seem to be becoming fact...")
    print_slow("\nThat's why you're here, after all.")
    print_slow("""
The mist stirs ahead of you... and suddenly you can see it - """, '')
    print_slow("the famed door!")
    print_slow("\nYour heartrate increases as you knock on it...")
    print("\n")


def part_two():
    """Plays out and prints situation for part two."""
    print_slow("""
You step cautiously forwards through the door, unsure what to expect. """, '')
    print_slow("It closes behind you.")
    print_slow("\nAhead, a noise. ", '')
    print_slow("Something stirs as you strike a match... ")
    print_slow("\nSnap -  it's charging! You ready for combat.", wait=3)
    print("\n\n--BATTLE--")
    battle(1, user, "user")
    print("----------\n")
    if not user.get_status():
        raise Dead("player is dead")
    sleep(3)
    print_slow("\nSome test. ", '')
    print_slow("Or was it a test? ", '')
    print_slow("Was it even meant to be there?")
    print_slow("\nUnderneath the vanquished enemy you spot a note.")
    print_slow("\nIt reads 'head to the heart of the forest'.")
    print_slow("\nThat definitely has to be a test.")
    user.increase_defence(2)
    print_slow("""
Before you set off you fortify your teeth with all the dental treatments you're
aware of (defence has increased by 2).""")
    print()


def part_three():
    """Plays out and prints situation for part three."""
    print_slow("\nYou know of two methods for getting there")
    print_slow("(1) the main road out of town")
    print_slow("(2) out the back and round through the fens")
    route = ""
    while route not in FOREST_ROUTES.values():
        route = input("Which route will you take? ")
        if route not in FOREST_ROUTES.values():
            try:
                route = FOREST_ROUTES[route]
            except KeyError:
                print("You set off, but shortly realise it isn't a route...")
    if route == "main road":
        print_slow("\nThe main road it is.")
    else:
        print_slow("\nThrough the fens it is! Watch your step...")
    print_slow("""
You march purposefully and wholly uneventfully for half a day. """, '')
    print_slow("Then, as nothing continues to happen, you keep marching.")
    print_slow("""
By midafternoon you can see the forest, your destination easily in sight.""")
    print_slow("\n500m... ", '')
    print_slow("200m... ", '')
    print_slow("100m...")
    print_slow("\nWait... what on earth is that obstructing the entrance?!")
    print_slow("Yeurch.", wait=3)
    print("\n\n--BATTLE--")
    battle(1, user, end_msg=FOREST_OUTSKIRTS_ENCOUNTER)
    print("----------\n")
    if not user.get_status():
        raise Dead("player is dead")
    sleep(3)
    print_slow("\nA little way into the forest you come to a small township.")
    print_slow("\nThe folk about seem restless. ", '')
    print_slow("Understandable given the state of the kingdom.")
    print_slow("\nOne in particular seems to be trying to catch your eye.")
    print_slow("(1) go over to them")
    print_slow("(2) ignore them, they are beneath you")
    choice = input("What do you do? ")
    while choice not in ("1", "2"):
        print("Alas, that isn't an option (1/2)...")
        choice = input("What do you do? ")
    if choice == "1":
        print_slow("\nThe local smiles at you gratefully.")
        print_slow("\n'You look like you're trying to achieve something.'")
        print_slow("(1) I am indeed")
        print_slow("(2) Not sure yet...")
        response = input("What do you reply? ")
        while response not in ("1", "2"):
            print("You find yourself unable to say that...")
            response = input("What do you reply? ")
        if response == "1":
            print_slow("""
'Epic! Someone needs to. Here, take this, you may find it useful.'""")
        else:
            print_slow("""
'Weelll even if you don't I certainly won't. Take this trinket of mine, you may
find it useful.'""")
        user.add_attack("scaler")
        print_slow("\nThey've given you a scaler! ", '')
        print_slow("You thank the local profusely and carry on.")
        user.level_up()
    else:
        print_slow("\nYou march right by, nose held high. ", '')
        print_slow("Resentful looks are cast your way...")
    print_slow("\nAn eerie quiet ensues as you approach the heart... ", '')
    print_slow("like the wildlife is holding its breath...")
    print_slow("\nThen suddenly it isn't at all quiet.", wait=3)
    print("\n\n--BATTLE--")
    battle(3, user, msg=FOREST_MOB_MSG[0], end_msg=FOREST_MOB_MSG[1])
    print_slow("\nA closer inspection of the area reveals a treasure trove.")
    new_attack = random.choice(["toothpaste", "dental floss"])
    user.add_attack(new_attack)
    print_slow("\nAmong other things, ", '', wait=0.015)
    if new_attack == "dental floss":
        print_slow("you've found a packet of dental floss!")
    else:
        print_slow("you've found a tube of toothpaste!")
    print("----------\n")
    if not user.get_status():
        raise Dead("player is dead")
    sleep(3)
    print_slow("\nThe watchtower in the hills..? ", '')
    print_slow("You survey the recent battlefield. ")
    print_slow("""
However far these tests really extend, these creatures are evil.""")
    if choice == "1":
        print_slow("\nIt's like the local said. Someone has to do something.")
    else:
        print_slow("\nKilling them would grant you unmatched fame and glory.")
    print_slow("\nYou turn and head for the watchtower...")


def part_four():
    """Plays out and prints situation for part four."""
    print_slow("\nAfter half a day's trek you reach the watchtower. ", '')
    print_slow("I wonder what's inside... ", wait=3)
    print("\n\n--BATTLE--")
    mob = battle(4, user, msg=TWR_MB_MSG[0], end_msg=TWR_MB_MSG[1], name=True)
    print("----------\n")
    if not user.get_status():
        raise Dead("player is dead")
    sleep(3)
    print_slow("\nA search of the tower proves far more lucrative!")
    print_slow("\nIn an obscure draw you uncover a scrap of paper... ")
    print_slow("""
It reads 'We attack tomorrow. Tell your minions to move out.'""")
    print_slow(f"""
Evidently the {mob} was well up in the hierachy of these dental monsters.""")
    print_slow("""
The note is signed - presumably by the one behind it all! You make a note of it
before setting off.""")
    print_slow("\nCoca-Cola", '', gap=0.5, wait=0.015)
    print_slow(". That's interesting...")
    print_slow("\nYou set off back to the capital. Time for this to end.")
    user.level_up()


def part_five():
    """Plays out and prints situation for part five."""
    pass


def epilogue():
    """Prints the epilogue to the game."""
    pass


class Dead(Exception):
    """Raised if a user dies and therefore cannot finish the game."""

    def __init__(self, message=None):
        self.message = message


if __name__ == "__main__":
    try:
        # Run all parts (functions) in order
        prologue()
        user = Player()
        print()
        next_part(1, "what's behind the door?")
        part_two()
        next_part(2, "the heart of the forest,")
        part_three()
        next_part(3, "the truth,")
        part_four()
        next_part(4, "cracking it open,")
        part_five()
        epilogue()
    except Dead:
        # If the user dies part way through
        print_slow("\nBetter luck next time!")
