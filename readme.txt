(Really) Random Passwd
======================

This simple Python class uses the random.org api
to generate really secure passwords.

The class has 3 settings, one for using the standard
random number generator or the random.org service,
one for how secure (or simple) you want the password,
and one for the length of the password.

Example Use
===========

# Assign the class to p
p = RandomPasswd()

# Generate and print a password of length 8
# with a level 2 security.
print p.passwd(8, 2)

Licence
=======

Released under the MIT Licence.

See licence.txt.