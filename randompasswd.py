#!/usr/bin/env python3

# -*- coding: UTF8 -*-
#
# RandomPasswd
# ============
#
# This class provides a method of generating a secure password.
# Dependant on random.org and the python class found here:
# http://pypi.python.org/pypi/randomdotorg/
#
# Example useage:
#
# >>> from randompasswd import RandomPasswd
# >>> p = RandomPasswd()
# >>> print p.passwd([length], [strength], [amount])
#
# A password strength of 1 is low while 4 is very high.

__version__ = '1.1'
__url__ = 'https://github.com/r3morse/random-passwd'
__author__ = "Sam Parkinson <r3morse at gmail dot com>"
__license__ = "MIT Licence"

from randomdotorg import RandomDotOrg

import sys
import getopt
import random


class RandomPasswd:
    """This class can be used to generate secure passwords.

    To use, do something like the following:

    >>> from randompasswd import RandomPasswd
    >>> p = RandomPasswd()
    >>> print p.passwd()
    """

    # A list of characters that will be used to generate a password.
    lower = ['a', 'b', 'c', 'd', 'e', 'f', 'g', 'h', 'i', 'j', 'k', 'l', 'm',
             'n', 'o', 'p', 'q', 'r', 's', 't', 'u', 'v', 'w', 'x', 'y', 'z']

    upper = ['A', 'B', 'C', 'D', 'E', 'F', 'G', 'H', 'I', 'J', 'K', 'L', 'M',
             'N', 'O', 'P', 'Q', 'R', 'S', 'T', 'U', 'V', 'W', 'X', 'Y', 'Z']

    number = ['0', '1', '2', '3', '4', '5', '6', '7', '8', '9']

    punctuation = ['`', '!', '"', '$', '%', '^', '&', '*', '(', ')', '\'',
                   '-', '_', '=', '+', '[', '{', ']', '}', ';', ':', '?',
                   '@', '#', '~', '\\', '|', ',', '<', '.', '>', '/']

    # Creating the characters variable that will, according to the security
    # level contain a list of characters from the above lists.
    characters = list()

    # Our quota at random.org.
    quota = None

    # Start the random.org api class.
    r = RandomDotOrg()

    def set_security(self, strength):
        """Takes the given security strength and generates a mixed list for `characters`."""

        if strength < 0 or strength > 4:
            raise ValueError("Please enter a strength between 0 and 4.")

        if strength >= 0:
            self.characters = self.number

        if strength >= 1:
            self.characters += self.lower

        if strength >= 2:
            self.characters += self.upper

        if strength >= 3:
            self.characters += self.number

        if strength == 4:
            self.characters += self.punctuation

    def get_random_characters(self, length):
        """Retrives the random string of numbers for our password."""

        if type(length) is not int:
            raise TypeError("`length` must be an integer.")

        # Use the random.org API to get our random numbers.
        self.quota = self.r.get_quota()

        if self.quota > 0:
            numbers = list()

            numbers = self.r.randrange(0, len(self.characters), ammount=length)
        else:
            raise ValueError("Out of random.org bits...")

        characters = list()

        # Shuffle the list of characters we are using.
        self.r.shuffle(self.characters)

        for i in numbers:
            characters.append(self.characters[i])

        return characters

    def passwd(self, length=14, strength=4, amount=1):
        """Generates a strong password with a default length of 14.

        `length`   the length of the password(s).

        `strength` the strength of the password(s), 0 is low
                   4 is very high.

        `amount`   the number of passwords you would like to make,
                   when more than one is made, this function
                   returns a list of strings.
        """

        if type(amount) is not int or amount < 1:
            raise ValueError("`amount` needs to be a positive integer.")

        total_chars = length * amount

        # Avoid requesting too large an amount of random intgers.
        if total_chars > 10000:
            if length > amount:
                raise ValueError("Please request a smaller password length.")
            else:
                raise ValueError("Please generate a smaller number of passwords.")

        self.set_security(strength)

        random_characters = self.get_random_characters(total_chars)

        count = 0
        password = list()

        # Splice up the list of random_characters into seperate passwords.
        while count < total_chars:
            password.append(''.join(random_characters[count:count + length]))

            count += length

        return password

#
# Comand Line Usage
#

if __name__ == "__main__":
    p = RandomPasswd()

    length = 128
    strength = 4
    number = 1

    try:
            opts, args = getopt.getopt(sys.argv[1:], "l:s:n:", ["length=", "strength=", "number="])
    except:
            usage()
            sys.exit(2)

    for opt, arg in opts:
            if opt == "-l":
                    length = int(arg)

            elif opt == "-s":
                    strength = int(arg)

            elif opt == "-n":
                    number = int(arg)

    result = p.passwd(length, strength, number)

    for password in result:
        print(password)


def usage():
        print("Unknown arguments.")
