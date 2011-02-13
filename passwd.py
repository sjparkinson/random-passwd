# -*- coding: UTF8 -*-
#
# This class (Password) provides a method of generating a password using
# random data from random.org (thanks to Clovis Fabricio: http://pypi.python.org/pypi/randomdotorg/)
#
# To use, use the function gen_password() in the form:
#
# p = Password()
# password = p.gen_password(length, security_level[1-4])
#
# Security level 1 is low and 4 is high.

# 1 for internet, 0 for random module
rand_method = 0

if rand_method == 1:
    from randomdotorg import RandomDotOrg
    r = RandomDotOrg() 
else:
    import random

class Password():

    # A list of characters that will be used to generate a password.
    lower = [ "a", "b", "c", "d", "e", "f", "g", "h", "i", "j", "k", "l", "m",
              "n", "o", "p", "q", "r", "s", "t", "u", "v", "w", "x", "y", "z" ]

    upper = [ "A", "B", "C", "D", "E", "F", "G", "H", "I", "J", "K", "L", "M",
              "N", "O", "P", "Q", "R", "S", "T", "U", "V", "W", "X", "Y", "Z" ]

    num   = [ "0", "1", "2", "3", "4", "5", "6", "7", "8", "9" ]

    sym   = [ "`", "!", "\"", "$", "%", "^", "&", "*", "(", ")",
              "-", "_", "=", "+", "[", "{", "]", "}", ";", ":", "'",
              "@", "#", "~", "\\", "|", ",", "<", ".", ">", "/", "?" ]

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
            self.chars = self.chars + self.num
        if level == 4:
            self.chars = self.chars + self.sym
            
    # Function retrives the random string of numbers required to generate a password
    # from random.org
    def get_randnums(self, length):
        data = list()

        # Use the random.org API to get our random numbers
        if rand_method == 1:
            quota = r.get_quota()
        
            if self.quota > 0:
                # print "Bits quota left: " + str(self.quota)
                data = r.randrange(1, len(self.chars), 1, ammount = length)
            else:
                raise ValueError("Out of random.org bits :/")

        # Use the psudorandom number generator in python
        else:
            i = 0
            while i < length:
                data.append(random.randrange(1, len(self.chars), 1))
                i = i + 1
                
        return data            

    # Converts the lost of numbers into a list of characters using the chars var
    def converter(self, numbers):
        data = list()

        for i in numbers:
            data.append(self.chars[i])

        return data

    # Generates a string of the actual password from the list of characters
    def password(self, letters):
        password = str()

        for i in letters:
            password = password + i

        return password

    # The public method for generating a password, input is length of password and security level
    def gen_password(self, length, level):
        if (level >= 1 and level <= 4):
            self.set_security(int(round(level)))
        else:
            return "Please enter a security level between 1 and 4."
        
        # print "Security: " + str(level)
        # print "Length:   " + str(length)
        
        rand     = self.get_randnums(length)
        letters  = self.converter(rand)
        password = self.password(letters)

        return password


# Example of how to generate a password
p = Password()
print p.gen_password(8, 1)
print p.gen_password(8, 2)
print p.gen_password(8, 3)
print p.gen_password(8, 4)
