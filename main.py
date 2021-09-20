##
# main.py
# Date: 08/09/2021
# Author: Ryan Gordon
# Plays as PRG game with the user as a dentist, promotes good dental hygiene

from time import sleep
from battle import battle
from player import Player
from print_options import print_slow


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
    print_slow("\nThat's why you're here, after all.")
    sleep(1)
    print_slow("""
The mist stirs ahead of you... and suddenly you can see it - """, '')
    sleep(1)
    print_slow("the famed door!")
    sleep(1)
    print_slow("\nYour heartrate increases as you knock on it...")
    sleep(1)
    print("\n")

if __name__ == "__main__":
    # Print prelude to character creation, then create the character
    print_prelude()
    user = Player()
    sleep(1)
    print("\n\n")
    # Sample battle with no context
    user = battle(1, user, "user")
