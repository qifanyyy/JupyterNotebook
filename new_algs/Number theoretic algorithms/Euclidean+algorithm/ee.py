'''extended euclidian algorithm'''
'''If d | a and d | b , then d | ax + by for any integers x and y .
gcd(a, b) is the smallest positive integer of the set  {ax + by : x, y ϵ Z} of linear combinations of a and b.
 ax + by = gcd(a, b)'''


def e(a, b):
    'eucledian'
    print(a, b)
    if b == 0:
        return a
    else:
        return ee(b, a % b)

def ee(a, b):
    'ectended eucledian'
    if b == 0:
        return (a, 1, 0)
    else:
        (dd, xx, yy) = ee(b, a % b)
        (d, x, y) = (dd, yy, xx - (a//b)*yy)
        print(d, x, y)
        return(d, x, y)



def poet(a,b):
    gcd, x, y = ee(a,b)
    print('ax + by = gcd(a,b)')
    print(f'{x}a {y}b = {gcd}')

poet(56, 15)

