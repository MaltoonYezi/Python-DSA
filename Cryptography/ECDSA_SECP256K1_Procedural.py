#Secp256k1 Bitcoin digital signing script (Procedural implemetation)
a = 0
b = 7
#Order of the finite field
prime = 2**256 - 2**32 - 977

#G coordinates
gx = 0x79be667ef9dcbbac55a06295ce870b07029bfcdb2dce28d959f2815b16f81798
gy = 0x483ada7726a3c4655da4fbfc0e1108a8fd17b448a68554199c47d08ffb10d4b8

#Order of the group G
n = 0xfffffffffffffffffffffffffffffffebaaedce6af48a03bbfd25e8cd0364141


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

def signing(privateKeyE, hashZ, n, randomNumberK, gx, gy, a, b, prime):
    Rx, Ry = secp256k1BinaryExpansion(randomNumberK, gx, gy, a, b, prime)
    k_inv = pow(randomNumberK, n-2, n)
    s = (hashZ + Rx * privateKeyE) * k_inv % n
    return (Rx, s)

def verification(Rx, s, n, gx, xPub, prime):

    s_inv = pow(s, n-2, n)
    u = hashZ * s_inv % n
    v = Rx * s_inv % n

    if ((u * gx) % prime + (v * xPub % prime)) == Rx:
        return "The signature is valid"
    else:
        return "The signature is valid"

#Test case 1

#n -1 => is the number of all possible private keys
privateKeyE = 0xa665a45920422f9d417e4867efdc4fb8a04a1f3fff1fa07e998e86f7f7a27ae3

#Hash of the message
hashZ = 0xbe347331b4d87273e674b30384985c639069f852246e8c128417dbb1ca8ba812

#randomly generated number
randomNumberK = 0x3f712500013085b1b082ffbfcc43c406cefdc97cd5a0977cf861356ed96a7642

#Creating public key points
xPub, yPub = secp256k1BinaryExpansion(privateKeyE, gx, gy, a, b, prime)

#Signature values
Rx, s = signing(privateKeyE, hashZ, n, randomNumberK, gx, gy, a, b, prime)

print("The point:", xPub, yPub)
print("Uncompressed public key:", "\n04", xPub, yPub)
print("Hash of the message:", hashZ)
print("The signature:")
print("r:", Rx)
print("s:", s)
print(verification(Rx, s, n, gx, xPub, prime))
