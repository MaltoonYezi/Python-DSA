prime = 223
a = 0
b = 7
#The curve is y^2 = (x^3) + ax + b

def otherFunction(x1, y1, x2, y2, a, b, prime):

    #Case 1 Both points are None
    if x1 is None and y1 is None and x2 is None and y2 is None:
        return (None, None)

    #Case 2: One of the points do not exist
    if x1 is None and y1 is None:
        return (x2, y2)
    elif x2 is None and y2 is None:
        return (x1, y1)

    #Case 3: One of the points are not on the curve
    if (y1 ** 2) % prime != ((x1 ** 3) + (a * x1) + b) % prime:
        return "The point P1 is not on the curve"
    if (y2 ** 2) % prime != ((x2 ** 3) + (a * x2) + b) % prime:
        return "The point P2 is not on the curve"

    #Case 4: X1 is not equal to X2
    if x1 != x2:
        s = ((y2 - y1) * (x2 - x1) ** (prime - 2)) % prime
        x = ((s ** 2) - x1 - x2) % prime
        y = ((s * (x1 - x)) - y1) % prime
        return (x, y)

    #Case 5: If P1 = P2 (Points are the same)
    if x1 == x2 and y1 == y2 and y1 != 0:
        s1 = (3 * (x1 ** 2) + a) % prime
        s2 = (y1 * 2) % prime
        s = (s1 * s2 ** (prime - 2)) % prime
        x = (s ** 2 - 2 * x1) % prime
        y = (s * (x1 - x) - y1) % prime
        return (x, y)

    #Case 6: Points are the same but y = 0
    if x1 == x2 and y1 == y2 and y1 == 0:
        return (None, None)

    #Case 7: Line is vertical (Point at infinity)
    if x1 == x2 and y1 != y2:
        return (None, None)

#Test
# (170,142) + (60,139)
print ( "The point is:",otherFunction(170, 142, 60, 139, a ,b, prime))
# (47,71) + (17,56)
print ( "The point is:", otherFunction(47, 71, 17, 56, a ,b, prime))
# (143,98) + (76,66)
print ( "The point is:", otherFunction(143, 98, 76, 66, a ,b, prime))
# (143,98) + (143,98)
print ( "The point is:", otherFunction(143, 98, 143, 98, a ,b, prime))
''' 
The right values:
Point(220,181)_0_7 FieldElement(223)
The point is: (220, 181)
Point(215,68)_0_7 FieldElement(223)
The point is: (215, 68)
Point(47,71)_0_7 FieldElement(223)
The point is: (47, 71)
Point(64,168)_0_7 FieldElement(223)
The point is: (64, 168)
'''