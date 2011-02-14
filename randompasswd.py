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
# >>> print p.passwd([length], [strength], [ammount])
#
# A password strength of 1 is low while 4 is very high.

__version__ = '1.1'
__url__ = 'https://github.com/r3morse/random-passwd'
__author__ = "Sam Parkinson <r3morse at gmail dot com>"
__license__ = "MIT Licence"

from randomdotorg import RandomDotOrg

class RandomPasswd():
    """This class can be used to generate secure passwords.

    To use do something like the following:
    
    >>> from randompasswd import RandomPasswd
    >>> p = RandomPasswd()
    >>> print p.passwd()
    """

    # A list of characters that will be used to generate a password.
    lower   = [ "a", "b", "c", "d", "e", "f", "g", "h", "i", "j", "k", "l", "m",
                "n", "o", "p", "q", "r", "s", "t", "u", "v", "w", "x", "y", "z" ]

    upper   = [ "A", "B", "C", "D", "E", "F", "G", "H", "I", "J", "K", "L", "M",
                "N", "O", "P", "Q", "R", "S", "T", "U", "V", "W", "X", "Y", "Z" ]

    number  = [ "0", "1", "2", "3", "4", "5", "6", "7", "8", "9" ]

    symbol  = [ "`", "!", "\"", "$", "%", "^", "&", "*", "(", ")", "'",
                "-", "_", "=", "+", "[", "{", "]", "}", ";", ":", "?",
                "@", "#", "~", "\\", "|", ",", "<", ".", ">", "/" ]

    # Creating the chars variable that will, according to the security level
    # contain a list of characters from the above lists.
    chars   = dict()

    # Our quota at random.org.
    quota   = None

    # Start the random.org api class.
    r = RandomDotOrg()

    def set_security(self, strength):
        """Takes the given security strength and generates a mixed list in `chars`."""
        strength = int(round(strength))
        
        if (strength >= 1 and strength <= 4):
            if strength >= 1:
                self.chars = self.lower
            if strength >= 2:
                self.chars = self.chars + self.upper
            if strength >= 3:
                self.chars = self.chars + self.number
            if strength == 4:
                self.chars = self.chars + self.symbol
        else:
            raise ValueError("Please enter a strength between 1 and 4.")
    
    def get_randnumbers(self, length):
        """Retrives the random string of numbers for our password."""
        if type(length) is type(int()):
            data = list()

            # Use the random.org API to get our random numbers
            self.quota = self.r.get_quota()
            
            if self.quota > 0:
                data = self.r.randrange(0, len(self.chars), ammount = length)
            else:
                raise ValueError("Out of random.org bits...")
                     
            return data
        else:
             raise TypeError("`length` must be an intger.")

    def list_2_char(self, numbers):
        """Converts the list of numbers into a list of characters using `chars`."""
        data = list()

        for i in numbers:
            data.append(self.chars[i])

        return data

    def gen_password(self, letters):
        """Generates string(s) of the actual password from the list `letters`."""
        password = str()

        for i in letters:
            password = password + i

        return password

    def passwd(self, length = 12, strength = 4, ammount = 1):
        """Generates a strong password with a default length of 12.
        
        `length`   the length of the password(s).
        
        `strength` the strength of the password(s), 1 is low
                   4 is very hiht.
        
        `ammount`  the number of passwords you would like to make,
                   when more than one is made, this function
                   returns a list of strings.
        """
        if type(ammount) is not type(int()) or ammount < 1:
            raise TypeError("`ammount` needs to be an intger.")

        self.set_security(strength)

        password = list()

        rand     = self.get_randnumbers(length * ammount)
        letters  = self.list_2_char(rand)

        i = 0
        start = 0
        end   = 0
        
        while i < ammount:
            end = length * (i + 1)
            password.append(self.gen_password(letters[start:end]))
            start = start + length
            i = i + 1

        if i is 1:
            password = str(password[0])

        return password
