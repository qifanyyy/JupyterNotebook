import sys

# base 10000 pi spigot algorithm
#
# translated from C:
#     http://stackoverflow.com/questions/4084571/implementing-the-spigot-algorithm-for-%CF%80-pi
#
#    // Spigot program for pi to NDIGITS decimals.
#    // 4 digits per loop.
#    // Thanks to Dik T. Winter and Achim Flammenkamp who originally made a compressed version of this. 
#

def verify(digits_of_pi, N):
    from hashlib import sha1

    first_100 = (
                    '31415926535897932384'
                    '62643383279502884197'
                    '16939937510582097494'
                    '45923078164062862089'
                    '98628034825342117067'
                )

    # sha1 hashes of the first n digits of pi from
    #     https://www.angio.net/pi/digits.html

    v = dict()
    v[1000] = 'a03730e0b961b25376bb0623a6569d61af301161'
    v[ 500] = 'c09d63fcaae39f2a53e3f7425b36f47e7060da86'
    v[ 100] = '756f5c5d68d87ef466dd656922d8562c7a499921'

    def _hash_verify(D, dop=digits_of_pi):
        b = bytes(dop[0:D], 'utf-8')
        assert sha1(b).hexdigest() == v[D]
        print('** Verified first {} digits of pi'.format(D), file=sys.stderr)

    def _startswith_verify(D, dop=digits_of_pi):
        assert first_100.startswith(dop)
        print('** Verified first {} digits of pi'.format(D), file=sys.stderr)

    if N >= 1000:
        _hash_verify(1000)   
    elif N >= 500:
        _hash_verify(500)
    elif N >= 100:
        _hash_verify(100)
    else:
        _startswith_verify(N)

# The below is more or less a straight word-for-word translation from C. It's not pretty.
#
# I'm not really clear on the big O but it looks like N**2. 1M digits takes a really long time.
#
# TODO:
#
# * Needs real variable names (requires better understanding of the math)
# * More explicit loop control (requires loop refactoring, which requires better understanding)
#
# * The magic numbers are:
#     10000, base of the numbers generated
#      2000, pi is 22222222... in the algorithms "native" base, not sure about the factor 1k
#        14, related to log2(base)
#         4, number of characters per base 10000 digit
#   Once I understand the math better I could come up with names for the magic numbers
#
# * For extra points, I could use cython to speed things up a bit
#

def pi_spigot_base10k(N):
    alen = int((N / 4 + 1) * 14)
    a = [ 0 ] * alen
    c = len(a)
    d = 0
    e = 0
    f = 10000
    h = 0

    while True:
        c -= 14
        b = c
        if b > 0:
            while True:
                b -= 1
                if b > 0:
                    d *= b
                    if h == 0:
                        d += 2000*f
                    else:
                        d += a[b]*f
                    g = b + b - 1
                    a[b] = d % g
                    d //= g
                else:
                    break
            h = str(e + d//f).zfill(4)
            yield h
            e = d % f
            d = e
        else:
            break

if __name__ == '__main__':
    try:
        N = int(sys.argv[1])
    except (IndexError, ValueError):
        N = 100

    assert N > 3 # algorith breaks down for fewer than 4 digits

    digits_of_pi = (''.join(pi_spigot_base10k(N)))[0:N]
    print(digits_of_pi)
    verify(digits_of_pi, N)

