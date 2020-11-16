'''
    XorEncrypt uses exclusive or bitwise operations to encrypt a string
    given a key.
    For instance given 'A' and 'z'

    A has char code of 65  or in bin 01000001
    z has char code of 122 or in bin 01111010

    XOR these gives:
    00111011 or 59 in dec

    Which represents character ';'


    :param  str     plain       String to encrypt
    :param  str     key         String representing key

    :return string
'''
def encrypt(plain, key):
    assert(isinstance(plain, str) and isinstance(key, str))
    assert(len(plain) > 0 and len(key) > 0)
    return ''.join([chr(ord(l) ^ ord(key[i % len(key)])) for i, l in enumerate(plain)])
