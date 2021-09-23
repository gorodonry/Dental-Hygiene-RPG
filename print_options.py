##
# print_options.py
# Date: 09/09/2021
# Author: Ryan Gordon
# Contains options for printing lines slowly

from time import sleep
import sys


def print_slow(message, newline='\n', gap=0.015, wait=1.5):
    """
    Prints a line one character at a time.

    Used to enhance user experience while playing the game.
    """
    for character in list(message):
        print(character, end='')
        sleep(gap)
    print(end=newline)
    sleep(wait)


def print_red(message):
    """Prints a line of text in red."""
    sys.stderr.write(message + '\n')
