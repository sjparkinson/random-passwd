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
__url__     = 'https://github.com/r3morse/random-passwd'
__author__  = "Sam Parkinson <r3morse at gmail dot com>"
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
    lower       = [ "a", "b", "c", "d", "e", "f", "g", "h", "i", "j", "k", "l", "m",
                                    "n", "o", "p", "q", "r", "s", "t", "u", "v", "w", "x", "y", "z" ]

    upper       = [ "A", "B", "C", "D", "E", "F", "G", "H", "I", "J", "K", "L", "M",
                                    "N", "O", "P", "Q", "R", "S", "T", "U", "V", "W", "X", "Y", "Z" ]

    number      = [ "0", "1", "2", "3", "4", "5", "6", "7", "8", "9" ]

    punctuation = [ "`", "!", "\"", "$", "%", "^", "&", "*", "(", ")", "'",
                                     "-", "_", "=", "+", "[", "{", "]", "}", ";", ":", "?",
                                     "@", "#", "~", "\\", "|", ",", "<", ".", ">", "/" ]

    # Creating the characters variable that will, according to the security level
    # contain a list of characters from the above lists.
    characters = dict()

    # Our quota at random.org.
    quota = None

    # Start the random.org api class.
    r = RandomDotOrg()

    def set_security(self, strength):
        """Takes the given security strength and generates a mixed list in `characters`."""

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

    def get_randnumbers(self, length):
        """Retrives the random string of numbers for our password."""

        if type(length) is not int:
            raise TypeError("`length` must be an integer.")

        # Use the random.org API to get our random numbers.
        self.quota = self.r.get_quota()

        if self.quota > 0:
            data = list()

            data = self.r.randrange(0, len(self.characters), ammount = length)
        else:
            raise ValueError("Out of random.org bits...")

        return data

    def list_2_char(self, numbers):
        """Converts the list of numbers into a list of characters using `characters`."""

        data = list()

        # shuffle the list of characters we are using.
        self.r.shuffle(self.characters)

        for i in numbers:
            data.append(self.characters[i])

        return data

    def gen_password(self, letters):
        """Generates a string of the actual password from the list `letters`."""

        password = str()

        for i in letters:
            password = password + i

        return password

    def passwd(self, length = 14, strength = 4, amount = 1):
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

        # Avoid requesting too large an amount of random intgers.
        if length * amount > 10000:
            if length > amount:
                raise ValueError("Please request a smaller password length.")
            else:
                raise ValueError("Please generate a smaller number of passwords.")

        self.set_security(strength)

        rand     = self.get_randnumbers(length * amount)
        letters  = self.list_2_char(rand)

        # Splice up the list of letters into seperate passwords.
        i       = 0
        start   = 0
        end     = 0

        password = list()

        while i < amount:
            end = length * (i + 1)
            password.append(self.gen_password(letters[start:end]))
            start = start + length
            i = i + 1

        # Return a string if there is only one password.
        if i is 1:
            password = str(password[0])

        return password

#
# Comand Line Usage
#

if __name__ == "__main__":
    p = RandomPasswd()

    length = 64
    strength = 3
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

    result =  p.passwd(length, strength, number)

    if type(result) == str:
        print(result)
    else:
        for password in result:
             print(password)

def usage():
        print("Unknown arguments.")