##
# print_options.py
# Date: 09/09/2021
# Author: Ryan Gordon
# Contains options for printing lines slowly

from time import sleep


def print_slow(message, newline='\n', gap=0.01, wait=1):
    """
    Prints a line one character at a time.

    Used to enhance user experience while playing the game.
    """
    for character in list(message):
        print(character, end='')
        sleep(gap)
    print(end=newline)
    sleep(wait)
