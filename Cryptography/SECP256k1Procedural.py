#Secp256k1 Bitcoin private to public key converter script (Procedural implemetation)
a = 0
b = 7
#Order of the finite field
prime = 2**256 - 2**32 - 977
#G coordinates
gx = 0x79be667ef9dcbbac55a06295ce870b07029bfcdb2dce28d959f2815b16f81798
gy = 0x483ada7726a3c4655da4fbfc0e1108a8fd17b448a68554199c47d08ffb10d4b8
#Order of the group G
n = 0xfffffffffffffffffffffffffffffffebaaedce6af48a03bbfd25e8cd0364141
#n -1 => is the number of all possible private keys
privateKey = 0xfffffffffffffffffffffffffffffffebaaedce6af48a03bbfd25e8cd0364140

def addition(currentX, currentY, gx, gy, a, b, prime):
    if gy == 0:
        return (None, None)
    elif currentX is None and currentY is None:
        return (gx, gy)
    elif currentX == gx and currentY != gy:
        return (None, None)
    elif currentX == gx and currentY == gy and currentY == 0:
        return (None, None)
    elif currentX == gx and currentY == gy:
        s1 = (3 * pow(gx, 2, prime) + a) % prime
        s2 = (gy * 2) % prime
        s = (s1 * pow(s2, (prime - 2), prime)) % prime
        currentX = (s ** 2 - 2 * gx) % prime
        currentY = (s * (gx - currentX) - gy) % prime
    elif currentX != gx:
        s1 = (currentY - gy)
        s2 = (currentX - gx)
        s = (s1 * pow(s2, (prime - 2), prime)) % prime
        currentX = ((s ** 2) - gx - currentX) % prime
        currentY = ((s * (gx - currentX)) - gy) % prime

    return (currentX, currentY)


def secp256k1BinaryExpansion(privateKey, gx, gy, a, b, prime):
    if pow(gy, 2, prime) != (pow(gx, 3, prime) + a * gx + b) % prime:
        return "The point is not on the curve"
    coef = privateKey
    currentX, currentY = gx, gy
    resultX, resultY = None, None
    while coef:
        if coef & 1:
            resultX, resultY = addition(resultX, resultY, currentX, currentY, a, b, prime)
        currentX, currentY = addition(currentX, currentY, currentX, currentY, a, b, prime)
        coef >>= 1
    return (resultX, resultY)

#privateKey, gx, gy, a, b, prime
#Smaller numbers (Not Secp256k1). Right output for this is: (116, 55)
print(secp256k1BinaryExpansion(8, 47, 71, a, b, 223))

#Test case 2
priv = 0x45300f2b990d332c0ee0efd69f2c21c323d0e2d20e7bfa7b1970bbf169174c82
xPub, yPub = secp256k1BinaryExpansion(priv, gx, gy, a, b, prime)
print("Public key coordinates:", xPub,",", yPub)
#The right values for test case 2:
#x = 40766947848522619068424335498612406856128862642075168802372109289834906557916
#y = 70486353993054234343658342414815626812704078223802622900411169732153437188990

#Test case 2.1. Full Pulic key for test case 2:
print("Public key (hex), (Uncompressed) :", "04" + (str(hex(xPub)[2:])) + (str(hex(yPub)[2:])))
#The right public key (Uncormpressed):
#045A2146590B80D1F0D97CC7104E702011AFFF21BFAF817F5C7002446369BA9DDC9BD5DCD1B4A737244D6BB7B96E256391B8597D3A7972A6F8CA9096D4AEA1F37E
print("Public key (hex), (Compressed) :", "02" + (str(hex(xPub)[2:])))
#The right public key (Compressed):
#025A2146590B80D1F0D97CC7104E702011AFFF21BFAF817F5C7002446369BA9DDC
