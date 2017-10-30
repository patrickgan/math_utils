# Math Worksheet Generator (mathgen.py)

from functools import reduce
from fractions import gcd
from math import sqrt

import random
import sys, os.path

try:
    arg = sys.argv[1]
    num = sys.argv[2]
    outFile = sys.argv[3]
except IndexError as e:
    pass
finally:
    pass


# Generate Random Numbers Using a Function with a Short Name

def r(a,b):
    """ Generates some non-zero numbers from a to b. (or a-1 if a is negative and b is positive) """
    # numbers = range(a,0) + range(0,b)
    # return random.choice(numbers)
    number = random.randint(a,b)
    if number > 0:
        return number
    else:
        return number - 1

# FOIL and the Quadratic Formula

def foil(a,b,c,d):
    """ Takes two binomials (ax + b) * (cx + d) and foils them.
    Inputs should have GCD of 1 or -1.
    Returns the result in the form of (A,B,C) so can be used by quadratic(). """
    GCD = abs(reduce(gcd,(a,b,c,d)))
    for num in (a,b,c,d):
        num = num // GCD
    return (a*c, a*d + b*c, b*d) # I like this. So much more modular than the old foil().

def quadratic(a,b,c):
    discriminant = b**2 - 4*a*c # discriminant
    return ((-b + sqrt(discriminant))/(2*a),(-b - sqrt(discriminant))/(2*a))

# Classes to Handle FOIL and Quadratics For Worksheet Printing

class Foil:
    """ Quadratic equation factors. For foiling. Currently only uses integers. """
    def __init__(self,a,b,c,d,reduced_numbers=1):
        if reduced_numbers:
            GCD = abs(reduce(gcd,(a,b,c,d)))
        else:
            GCD = 1

        self.a = abs(a) // GCD # take the abs because it's easier to teach with positive coefficients for x^2
        self.b = b // GCD
        self.c = abs(c) // GCD
        self.d = d // GCD
        self.solution = str(solve(self))
    def __repr__(self):
        return 'Foil(%r, %r, %r, %r)' % (self.a, self.b, self.c, self.d)
    def __str__(self):
        def x(n):
            if n == 1:
                return 'x '
            else:
                return str(n) + 'x '
        def y(n):
            if n < 1:
                return '- ' + str(-n)
            else:
                return '+ ' + str(n)
        return '(' + x(self.a) + y(self.b) + ') * (' + x(self.c) + y(self.d) + ')'
    def solve(self):
        def foil(a,b,c,d):
            return Quadratic(a*c, a*d + b*c, b*d)
        return foil(self.a, self.b, self.c, self.d)


class Quadratic:
    """ Quadratic equation class. Currently only uses integers. """
    def __init__(self, a, b, c):
        self.a = a
        self.b = b
        self.c = c
        self.solution = solve(self)
    def __repr__(self):
        return 'Quadratic(%r,%r,%r)' % (self.a, self.b, self.c)
    def __str__(self):
        def x2(n):
            if n == 1:
                return 'x^2 '
            else:
                return str(n) + 'x^2 ' # doesn't matter if it's negative since it's first coefficient
        def x(n):
            if n < 1:
                if n == -1:
                    return '- ' + 'x '
                return '- ' + str(-n) + 'x '
            else:
                if n == 1:
                    return '+ ' + 'x '
                return '+ ' + str(n) + 'x '
        def y(n):
            if n < 1:
                return '- ' + str(-n)
            else:
                return '+ ' + str(n)
        return x2(self.a) + x(self.b) + y(self.c)
    def solve(self):
        def quadratic(a,b,c):
            discriminant = b**2 - 4*a*c # discriminant
            return ((-b + sqrt(discriminant))/(2*a),(-b - sqrt(discriminant))/(2*a))
        return quadratic(self.a, self.b, self.c)
    # to do: vertex form?
    def vertex(self):
        def complete_square(a,b,c):
            pass
        pass

class Conic:
    pass #todo?

def solve(math_class_object):
    """ If an object has a solve method, use it. Otherwise return object. """
    try:
        return math_class_object.solve()
    except AttributeError as e:
        return math_class_object

# Random Stuff

def twentyfour():
    """ Generates four numbers from 1 to 10. """
    result = ""
    for k in range(0,4):
        result += str(r(1,10)) + " "
    return result + "\n"

def pascal_gen(n):
    """
    Yield up to row `n` of Pascal's triangle, one row at a time.

    The first row is row 0.

    taken from http://www.bedroomlan.org/coding/pascals-triangle-python
    """
    def newrow(row):
        "Calculate a row of Pascal's triangle given the previous one."
        prev = 0
        for x in row:
            yield prev + x
            prev = x
        yield 1

    prevrow = [1]
    yield prevrow
    for x in range(n):
        prevrow = list(newrow(prevrow))
        yield prevrow

def pascal(n):
    """ returns the nth row of pascal's triangle """
    return list(pascal_gen(n))[n]

def binomial(a,b,c,var="x"):
    """ c > 1 """
    if a == 1:
        string = var + "^" + str(c) + " + "
    else:
        string = str(a**c) + var + "^" + str(c) + " + "
    coefficients = pascal(c)
    for n in range(1,c):
        string += str(coefficients[n] * a**(c-n) * b**n) + var + "^" + str(c-n) + " + " 

    if b == 1:
        string += "1"
    else:
        string += str(b**c)
    return string

# print(binomial(2,2,2))


# Run the program. TODO: fix so I can use this with the new classes.

if 'arg' in globals():
    if 'outFile' not in globals():
        outFile = 'output.txt'
    if 'num' not in globals():
        num = 1
    else:
        num = int(num)
    if arg=="foil": 
        a, b = -5, 10
        with open(outFile,'w') as o: 
            for k in range(1,num+1):
                f = Foil(r(a,b),r(a,b),r(a,b),r(a,b))
                o.write('{0}. {1}\n{2}\n\n'.format(k,f,f.solve()))
                # o.write(str(k) + ". " + f[0]+'\n')
                # o.write(f[1]+'\n\n')
        print("Complete.")
    elif arg=="twentyfour":
        with open(outFile,'w') as o:
            while num > 0:
                o.write(twentyfour())
                num-=1
        print("Complete.")
    elif arg=="binomial":
        print("Binomial expanision support currently not available.")
    elif arg=="exponent":
        print("Exponent problem support currently not available.")
    else:
        print("Usage: Enter a problem type and the number of instances.\nTypes: foil, twentyfour")


# if 'outFile' in globals():
#   with open(outFile,'w') as o: # r = read, w = write, a = append
#     for  in hitobjectstr:
      # o.write(str(i)+'\n')
