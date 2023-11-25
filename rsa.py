import random
import sympy

import binascii

def generateKeys(keysize=1024):
    e = d = N = 0
    # get prime nums, p & q
    p = generateLargePrime(keysize)
    q = generateLargePrime(keysize)
    print(f"p: {p}")
    print(f"q: {q}")

    N = p * q  # RSA Modulus
    phiN = (p - 1) * (q - 1)  # totient

    # choose e
    # e is coprime with phiN & 1 < e <= phiN
    while True:
        e = random.randrange(2 ** (keysize - 1), 2 ** keysize - 1)
        if (isCoPrime(e, phiN)):
            break

    # choose d
    # d is mod inv of e with respect to phiN, e * d (mod phiN) = 1
    d = modularInv(e, phiN)

    return ((e,N),( d, N))


def generateLargePrime(bitlength):
    """
        return random large prime number of keysize bits in size
    """
    a = '1' + '0' * (bitlength - 1)
    b = '1' * bitlength
    p = sympy.randprime(int(a, 2), int(b, 2))
    return p


def isCoPrime(p, q):
    """
        return True if gcd(p, q) is 1
        relatively prime
    """

    return gcd(p, q) == 1


def gcd(p, q):
    """
        euclidean algorithm to find gcd of p and q
    """

    while q:
        p, q = q, p % q
    return p


def egcd(a, b):
    s = 0;
    old_s = 1
    t = 1;
    old_t = 0
    r = b;
    old_r = a

    while r != 0:
        quotient = old_r // r
        old_r, r = r, old_r - quotient * r
        old_s, s = s, old_s - quotient * s
        old_t, t = t, old_t - quotient * t

    # return gcd, x, y
    return old_r, old_s, old_t


def modularInv(a, b):
    gcd, x, y = egcd(a, b)

    if x < 0:
        x += b

    return x


def encrypt(msg,package):
    e,N=package
    cipher = ""
    # print(format(msg, "08b"))

    if msg > N:
        print('Message is too large for key to handle')
    msg_ciphertext = pow(msg, e, N)

    # print(format(msg_ciphertext, "08b"))
    # print ('{0:08b}'.format(msg_ciphertext))
    return msg_ciphertext

def decrypt(msg_ciphertext, package):
    d, n = package
    msg_plaintext = pow(msg_ciphertext, d, n)

    return binascii.unhexlify(hex(msg_plaintext)[2:]).decode()
