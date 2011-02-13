# -*- coding: UTF8 -*-
#
# This class (RandomPasswd) provides a method of generating a password using
# random data from random.org (thanks to Clovis Fabricio: http://pypi.python.org/pypi/randomdotorg/)
#
# To use, use the function passwd() in the form:
#
# p = RandomPasswd()
# password = p.passwd(length, security_level[1-4])
#
# Security level 1 is low, 4 is high.

from randomdotorg import RandomDotOrg

r = RandomDotOrg()

class RandomPasswd():

    # A list of characters that will be used to generate a password.
    lower   = [ "a", "b", "c", "d", "e", "f", "g", "h", "i", "j", "k", "l", "m",
                "n", "o", "p", "q", "r", "s", "t", "u", "v", "w", "x", "y", "z" ]

    upper   = [ "A", "B", "C", "D", "E", "F", "G", "H", "I", "J", "K", "L", "M",
                "N", "O", "P", "Q", "R", "S", "T", "U", "V", "W", "X", "Y", "Z" ]

    number  = [ "0", "1", "2", "3", "4", "5", "6", "7", "8", "9" ]

    symbol  = [ "`", "!", "\"", "$", "%", "^", "&", "*", "(", ")", "'",
                "-", "_", "=", "+", "[", "{", "]", "}", ";", ":", "?",
                "@", "#", "~", "\\", "|", ",", "<", ".", ">", "/" ]

    quota   = None

    # Creating the chars variable that will, according to the security level
    # contain a list of characters from the above lists.
    chars = dict()

    # Takes the given security level and generates a mixed list for the chars var
    def set_security(self, level):
        level = int(round(level))
        
        if (level >= 1 and level <= 4):
            if level >= 1:
                self.chars = self.lower
            if level >= 2:
                self.chars = self.chars + self.upper
            if level >= 3:
                self.chars = self.chars + self.number
            if level == 4:
                self.chars = self.chars + self.symbol
        else:
            raise TypeError("Please enter a security level between 1 and 4.")
            
    # Function retrives the random string of numbers required to generate a password
    # from random.org
    def get_randnumbers(self, length):
        if type(length) is type(int()):
            data = list()

            # Use the random.org API to get our random numbers
            self.quota = r.get_quota()
            
            if self.quota > 0:
                # print "Bits quota left: " + str(self.quota)
                data = r.randrange(1, len(self.chars), 1, ammount = length)
            else:
                raise ValueError("Out of random.org bits :/")
                     
            return data
        else:
             raise TypeError("The length must be an intger.")

    # Converts the list of numbers into a list of characters using the chars var
    def list_2_char(self, numbers):
        data = list()

        for i in numbers:
            data.append(self.chars[i])

        return data

    # Generates a string of the actual password from the list of characters
    def gen_password(self, letters):
        password = str()

        for i in letters:
            password = password + i

        return password

    # The public method for generating a password, input is length of password and security level
    # default is a length of 4, security level 4 and ammount of 1.
    def passwd(self, length = 12, level = 4, ammount = 1):
        if type(ammount) is not type(int()) or ammount < 1:
            raise TypeError("Ammount needs to be an intger.")

        self.set_security(level)

        password = list()
        i = 0
        
        while i < ammount:
            rand     = self.get_randnumbers(length)
            letters  = self.list_2_char(rand)
            password.append(self.gen_password(letters))
            i = i + 1

        if i is 1:
            password = str(password[0])

        return password
