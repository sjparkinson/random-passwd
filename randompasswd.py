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
        if level >= 1:
            self.chars = self.lower
        if level >= 2:
            self.chars = self.chars + self.upper
        if level >= 3:
            self.chars = self.chars + self.number
        if level == 4:
            self.chars = self.chars + self.symbol
            
    # Function retrives the random string of numbers required to generate a password
    # from random.org
    def get_randnumbers(self, length):
        data = list()

        # Use the random.org API to get our random numbers
        self.quota = r.get_quota()
        
        if self.quota > 0:
            # print "Bits quota left: " + str(self.quota)
            data = r.randrange(1, len(self.chars), 1, ammount = length)
        else:
            raise ValueError("Out of random.org bits :/")
                
        return data            

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
    def passwd(self, length, level):
        if (level >= 1 and level <= 4):
            self.set_security(int(round(level)))
        else:
            return "Please enter a security level between 1 and 4."
        
        # print "Security: " + str(level)
        # print "Length:   " + str(length)
        
        rand     = self.get_randnumbers(length)
        letters  = self.list_2_char(rand)
        password = self.gen_password(letters)

        return password
