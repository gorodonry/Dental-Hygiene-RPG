##
# main.py
# Date: 08/09/2021
# Author: Ryan Gordon
# Plays as PRG game with the user as a dentist, promotes good dental hygiene

from time import sleep
from battle import battle
from player import Player
from print_options import print_slow
from constants import FOREST_ROUTES


def next_part(part, msg=''):
    """Prints a break in the story telling to signal a new 'chapter'."""
    print("\n-----")
    print_slow(f"End of part {part}.")
    to_print = f"\nPart {part + 1}{':' if msg != '' else ''} {msg} loadin"
    print_slow(to_print, '', wait=0)
    print_slow("g.....", gap=0.5, wait=0)
    print("-----\n")


def print_prelude():
    """Prints the prelude to the game."""
    print("Dental Hygiene RPG".center(80))
    print_slow("""
You walk up the empty street and turn left. """, '')
    print_slow("Another dark alleyway.")
    print_slow("""
The kingdom hasn't been the same lately; """, '')
    print_slow("""rumours of a great evil roaming across
the land have been circulating. """, '')
    print_slow("Rumours that seem to be becoming fact...")
    print_slow("\nThat's why you're here, after all.")
    print_slow("""
The mist stirs ahead of you... and suddenly you can see it - """, '')
    print_slow("the famed door!")
    print_slow("\nYour heartrate increases as you knock on it...")
    print("\n")


def part_one():
    """Plays out and prints situation for part one."""
    print_slow("""
You step cautiously forwards through the door, unsure what to expect. """, '')
    print_slow("It closes behind you.")
    print_slow("\nAhead, a noise. ", '')
    print_slow("Something stirs as you strike a match... ")
    print_slow("\nSnap -  it's charging! You ready yourself for combat.")
    sleep(2)
    print("\n\n--BATTLE--")
    # Fight a battle with a level 1 monster, user gets first strike
    battle(1, user, "user")
    print("----------\n")
    if not user.get_status():
        raise DeadError("player is dead")
    sleep(3)
    print_slow("\nSome test. ", '')
    print_slow("Or was it a test? ", '')
    print_slow("Was it even meant to be there?")
    print_slow("\nUnderneath the vanquished enemy you spot a note.")
    print_slow("\nIt reads 'head to the heart of the forest'.")
    print_slow("\nThat definitely has to be a test.")
    print()


def part_two():
    """Plays out and prints situation for part two."""
    print_slow("\nYou know of two methods for getting there")
    print_slow("(1) the main road out of town")
    print_slow("(2) out the back and round through the fens")
    route = ""
    # Ask user for route choice, loop until valid
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
    print_slow("Yeurch.")
    sleep(2)
    print("\n\n--BATTLE--")
    # Fight a battle with a level 1/2 monster, random first strike
    battle(2, user)
    print("----------\n")
    if not user.get_status():
        raise DeadError("player is dead")
    sleep(3)
    print_slow("""
It seems the dental theme isn't confined to the town... """, '')
    print_slow("interesting...")
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
        print("\n--LEVEL UP--")
        print_slow("Increased attack damage (by 2) and health (by 15)!")
        user.increase_max_health(15)
        user.heal_full()
        user.increase_attack_damage(2)
        print("------------")
    else:
        print_slow("\nYou march right by, nose held high. ", '')
        print_slow("Resentful looks are cast your way...")
    print_slow("\nAn eerie quiet ensues as you approach the heart... ", '')
    print_slow("like the wildlife is holding its breath...")
    print_slow("\nThen suddenly it isn't at all quiet.")
    sleep(2)
    print("\n\n--BATTLE--")
    # Fight a battle with a level 2 monster, random first strike
    battle(3, user)
    print("----------\n")
    if not user.get_status():
        raise DeadError("player is dead")
    sleep(3)
    ### CONTINUE FROM HERE


def part_three():
    pass


class DeadError(Exception):
    """Raised if a user dies and cannot finish the game."""

    def __init__(self, message=None):
        self.message = message

if __name__ == "__main__":
    try:
        # Print prelude to character creation, then create the character
        print_prelude()
        user = Player()
        print()
        next_part(1, "what's behind the door?")
        part_one()
        next_part(2, "the heart of the forest,")
        part_two()
        next_part(3, "the truth")
        part_three()
    except DeadError:
        # If the user dies part way through
        print_slow("\nBetter luck next time!")
