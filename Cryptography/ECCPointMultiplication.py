prime = 223
a = 0
b = 7
#The curve is y^2 = (x^3) + ax + b
#iterations - number by which we multiply the point

def ECCPointMultiplication(iterations,x1, y1,a,b, prime):
    if (y1 ** 2) % prime != (x1 ** 3 + a * x1 + b) % prime:
        return f'The point {x1, y1} is not on the curve'
    if y1 == 0:
        return "Infinity"
    for i in range(1, iterations):
        # First iteration
        if i == 1:
            s1 = (3 * (x1 ** 2) + a) % prime
            s2 = (y1 * 2) % prime
            s = (s1 * s2 ** (prime - 2)) % prime
            x = (s ** 2 - 2 * x1) % prime
            y = (s * (x1 - x) - y1) % prime
        else:
            # All other iterations
            # The point does not exist
            if x is None and y is None:
                return "Infinity"
            # Line is vertical (Point at infinity)
            elif x == x1 and y1 != y:
                return "Infinity"
            # Points are the same but y = 0
            elif x == x1 and y == y1 and y == 0:
                return "Infinity"
            else:
                s1 = (y - y1)
                s2 = (x - x1)
                s = (s1 * s2 ** (prime - 2)) % prime
                x = ((s ** 2) - x1 - x) % prime
                y = ((s * (x1 - x)) - y1) % prime
    return (x, y)

#Testing
# 2*(192, 105), right value: (49, 71)
print("The point is:",
      ECCPointMultiplication(2, 192, 105, a, b, prime))
# 2*(143, 98), right value: (64, 168)
print("The point is:",
      ECCPointMultiplication(2, 143, 98, a, b, prime))
# 2*(47, 71), right value: (36, 111)
print("The point is:",
      ECCPointMultiplication(2, 47, 71, a, b, prime))
# 4*(47, 71), right value: (194, 51)
print("The point is:",
      ECCPointMultiplication(4, 47, 71, a, b, prime))
# 8*(47, 71), right value: (116, 55)
print("The point is:",
      ECCPointMultiplication(8, 47, 71, a, b, prime))
# 21*(47, 71), right value: Infinity
print("The point is:",
      ECCPointMultiplication(21, 47, 71, a, b, prime))
