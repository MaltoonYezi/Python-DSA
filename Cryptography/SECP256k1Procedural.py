#Secp256k1 Bitcoin private to public key converter script (Procedural implemetation)
import hashlib

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

def uncompressed(xPub, yPub):
    if (xPub and yPub) != None:
        return "04" + (str(hex(xPub)[2:])) + (str(hex(yPub)[2:]))

def compressed(xPub, yPub):
    if yPub % 2 == 0:
        return "02" + (str(hex(xPub)[2:]))
    else:
        return "03" + (str(hex(xPub)[2:]))

def encode_base58(s):
    BASE58_ALPHABET = '123456789ABCDEFGHJKLMNPQRSTUVWXYZabcdefghijkmnopqrstuvwxyz'

    count = 0
    for c in s:
        if c == 0:
            count += 1
        else:
            break
    num = int.from_bytes(s, 'big')
    prefix = '1' * count
    result = ''
    while num > 0:
        num, mod = divmod(num, 58)
        result = BASE58_ALPHABET[mod] + result
    return prefix + result

def hash256(s):
    return hashlib.sha256(hashlib.sha256(s).digest()).digest()

def encode_base58_checksum(b):
    return encode_base58(b + hash256(b)[:4])

def wif(priv,compressed=True, testnet=False):
    secret_bytes = priv.to_bytes(32, 'big')
    if testnet:
        prefix = b'\xef'
    else:
        prefix = b'\x80'
    if compressed:
        suffix = b'\x01'
    else:
        suffix = b''
    return encode_base58_checksum(prefix + secret_bytes + suffix)

def hash160(s):
    return hashlib.new('ripemd160', hashlib.sha256(s).digest()).digest()

def address(pub, compressed=False, testnet=False):
    if compressed == True:
        h160 = hash160(pub.to_bytes(33, 'big'))
    else:
        h160 = hash160(pub.to_bytes(65, 'big'))
    if testnet:
        prefix = b'\x6f'
    else:
        prefix = b'\x00'
    return encode_base58_checksum(prefix + h160)

#privateKey, gx, gy, a, b, prime
#Smaller numbers (Not Secp256k1). Right output for this is: (116, 55)
print("Test case 1:\n", secp256k1BinaryExpansion(8, 47, 71, a, b, 223))

#Test case 2
priv = 0x45300f2b990d332c0ee0efd69f2c21c323d0e2d20e7bfa7b1970bbf169174c82
xPub, yPub = secp256k1BinaryExpansion(priv, gx, gy, a, b, prime)
print("\nTest case 2:")
print("Private Key (Hex)",hex(priv))
print("Private Key (WIF)", wif(priv,compressed=False, testnet=False))
#Right WIF: 5JLktXh2sfrYhEWjr6sskAGXBUUBdKUpawg8DPxYfB9iGmuP53o
print("Public key coordinates:", xPub,",", yPub)
#The right values for test case 2:
#x = 40766947848522619068424335498612406856128862642075168802372109289834906557916
#y = 70486353993054234343658342414815626812704078223802622900411169732153437188990

#Test case 2.1. Full Pulic key for test case 2:

print("Public key (hex), (Uncompressed) :", uncompressed(xPub, yPub))
#The right public key (Uncormpressed):
#045A2146590B80D1F0D97CC7104E702011AFFF21BFAF817F5C7002446369BA9DDC9BD5DCD1B4A737244D6BB7B96E256391B8597D3A7972A6F8CA9096D4AEA1F37E

print("Public key (hex), (Compressed) :", compressed(xPub, yPub))
#The right public key (Compressed):
#025A2146590B80D1F0D97CC7104E702011AFFF21BFAF817F5C7002446369BA9DDC

#Test case 2.2. Address
print("The address (Compressed): ",address(int(uncompressed(xPub, yPub), 16),compressed=False, testnet=False))
print("The address (Compressed): ",address(int(compressed(xPub, yPub), 16),compressed=True, testnet=False))
