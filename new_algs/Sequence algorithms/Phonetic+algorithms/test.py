from sounds import Soundex, Metaphone, isHomophone
from functools import partial

soundFromStart = partial(Soundex, start=True)

a = "Robert"
b = "Egbert"
c = "Rupert"
d = "Ashcraft"
e = "Ashcroft"
f = "Tymczak"
g = "fat"
h = "phat"
i = "jam"
j = "jamb"
k = "signet"
l = "signed"
m = "caught"
n = "cot"

assert isHomophone(a,c)
assert not isHomophone(a,b)
assert not isHomophone(b,c)
assert isHomophone(d,e)

assert Soundex(d) == "A261"
assert Soundex(f) == "T522"
assert not isHomophone(g,h)

assert isHomophone(g,h,algorithm=soundFromStart)

assert isHomophone(d,e, algorithm=Metaphone)
assert not isHomophone(a,b, algorithm=Metaphone)
assert not isHomophone(a,c, algorithm=Metaphone)
assert isHomophone(g,h, algorithm=Metaphone)
assert isHomophone(i,j, algorithm=Metaphone)
assert not isHomophone(k,l, algorithm=Metaphone)

assert isHomophone(m, n, algorithm=Metaphone)
