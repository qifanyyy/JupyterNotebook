#note: this code does not work
import sys


p = (13 << 28) + 1  #40961
n = 1 << 28
n_inv = 13
unit = 3 ** 13
r = 2 # two bits for each digit
#max input value: 2^r ^ n = 2 ^ 2 ^ (2 ^ 13) ~ 4900 digits


def setup():
    global p
    global n
    global unit
    global r
    global n_inv
    p = (3 << 6 )+ 1 #193
    n = 1 << 6
    r = 1
    unit = 5 ** 3 #125
    n_inv = 3


def mul(x, y):
    return x * y % p


def add(x, y):
    return (x + y) % p


def sub(x, y):
    return ((x - y) % p + p) % p


def pow(x, y):
    if y == 0:
        return 1
    if y == 1:
        return x
    t = pow(x, y >> 1)
    if y & 1:
        return mul(mul(t, t), x)
    return mul(t, t)


def calc_term(k):
    return pow(unit, k)


def bit_rev(x, l):
    return sum(1 << (l - 1 - i) for i in range(l) if (x >> i) & 1)


def bit_reverse(a):
    l = (len(a) - 1).bit_length()
    pos = [bit_rev(n, l) for n in range(len(a))]
    return [a[i] for i in pos]


unit_inv = calc_term(p - 2)


def fft_loop(a, l, pos):
    l1 = l >> 1
    if l > 1:
        fft_loop(a, l1,  pos)
        fft_loop(a, l1,  pos + l1)
    for i in range(l1):
        ide = i + pos
        ido = i + pos + l1
        term = mul(calc_term(i * n // l), a[ido])
        a[ido] = sub(a[ide], term)
        a[ide] = add(a[ide], term)


def fft_loop1(a, l, pos):
    l1 = l >> 1
    if l > 1:
        fft_loop1(a, l1,  pos)
        fft_loop1(a, l1,  pos + l1)
    for i in range(l1):
        ide = i + pos
        ido = i + pos + l1
        term = mul(pow(unit_inv, i * n // l), a[ido])
        a[ido] = sub(a[ide], term)
        a[ide] = add(a[ide], term)


def ifft(a):
    a_copy = bit_reverse(a[:] + [0] * (n - len(a)))
    fft_loop1(a_copy, len(a_copy),  0)
    return [mul(i, n_inv) for i in a_copy]



def fft(a):
    a_copy = bit_reverse(a[:] + [0] * (n - len(a)))
    fft_loop(a_copy, len(a_copy),  0)
    return a_copy


def gen_data():
    return 1233,1000


def split_data(a):
    ret = []
    while a > 0:
        ret.append(a & int('1' * r, 2))
        a >>= r
        if len(ret) > n:
            print("input size is too big", file = sys.stderr)
            sys.exit()
    return ret


def combine_data(arr):
    ret = 0
    for i in arr:
        ret <<= r
        ret += i
    return ret


def test_fft():
    a = [1, 5]
    print(a)
    print(fft(a))
    print(ifft(fft(a)))


def main():
    test_fft()
    return
    a, b = gen_data()
    a_arr = split_data(a)
    b_arr = split_data(a)
    a_fft = fft(a_arr)
    b_fft = fft(b_arr)
    c_fft = []
    for i in range(n):
        c_fft.append(mul(a_fft[i], b_fft[i]))
    c_arr = ifft(c_fft)
    c = combine_data(c_arr)
    print("a = %d" % a)
    print("b = %d" % b)
    print("a * b = %d" % (a * b))
    print("algorithm result = %d" % c)


setup()
main()
